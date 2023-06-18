import json
import time

from parser import models
import requests
from .scheme_processor import SchemeProcessor


class Parser:
    def __init__(self, site: models.Site):
        self.site = site
        self.processor = SchemeProcessor()

    def send_request(self, site, segment: models.Segment = None, token=None) -> dict:
        headers = {}
        body = {}
        params = {}
        if self.site.api_key:
            if self.site.api_key_place == models.ApiPlaceChoices.LINK:
                params[self.site.api_key_field_name] = self.site.api_key
            elif self.site.api_key_place == models.ApiPlaceChoices.BODY:
                body[self.site.api_key_field_name] = self.site.api_key
            elif self.site.api_key_place == models.ApiPlaceChoices.HEADER:
                headers[self.site.api_key_field_name] = self.site.api_key
        if segment and token:
            if segment.api_token_place == models.ApiPlaceChoices.LINK:
                params[segment.api_token_field_name] = token
            elif segment.api_token_place == models.ApiPlaceChoices.HEADER:
                headers[segment.api_token_field_name] = token
            elif segment.api_token_place == models.ApiPlaceChoices.BODY:
                body[segment.api_token_field_name] = token
        return requests.get(site, data=body, headers=headers, params=params).json()

    def process_response(self, response):
        scheme = self.site.json_scheme
        obj = self.processor.process(response, scheme)
        # print(obj)
        if self.site.first_run:
            segment_list = [[] for i in obj]
        else:
            segment_list = []
            for pair in obj:
                if len(models.Pair.objects.filter(site=self.site, token=pair)) == 0:
                    segment_list.append(self.parse_segments(pair))
                else:
                    segment_list.append([])
        pairs = zip(obj, segment_list)
        self.save_pairs(pairs)

    def parse_segments(self, pair):
        segments = []
        for segment in self.site.segment_set.filter(is_active=True):
            resource = self.send_request(segment.api_link, segment, pair)
            segment_str = self.processor.process(
                resource, segment.json_scheme, pair, segment.scheme_single_target_mode
            )
            if segment_str:
                segments.append({'json_name': segment.json_name, 'content': json.dumps(segment_str)})
        return segments

    def parse_site(self):
        response = self.send_request(self.site.list_api_link)
        self.process_response(response)

    def save_pairs(self, pairs):
        for pair in pairs:
            self.save_pair(*pair)

    def save_pair(self, pair, segments):
        saved_pair = models.Pair.objects.get_or_create(site=self.site, token=pair)[0]
        saved_pair.segments_loaded = len(segments) >= self.site.segment_set.count()
        for segment in segments:
            segment_instance = models.PairSegment.objects.get_or_create(
                pair=saved_pair,
                json_name=segment['json_name']
            )[0]
            if segment_instance.content != segment['content']:
                saved_pair.sent = False
                segment_instance.content = segment['content']
            segment_instance.save()
        saved_pair.save()
        self.site.first_run = False
        self.site.save()
