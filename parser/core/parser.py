import json
import time

from requests import JSONDecodeError

from parser import models
from .scheme_processor import SchemeProcessor
from requests.api import request


class Parser:
    def __init__(self, site: models.Site):
        self.site = site
        self.processor = SchemeProcessor()

    def send_request(self, site, segment: models.Segment = None, token=None) -> dict:
        headers = {}
        body = {}
        params = {}
        if self.site.api_key:
            if self.site.api_key_place == models.ApiPlaceChoices.PARAM:
                params[self.site.api_key_field_name] = self.site.api_key
            elif self.site.api_key_place == models.ApiPlaceChoices.BODY:
                body[self.site.api_key_field_name] = self.site.api_key
            elif self.site.api_key_place == models.ApiPlaceChoices.HEADER:
                headers[self.site.api_key_field_name] = self.site.api_key
            elif self.site.api_key_place == models.ApiPlaceChoices.LINK:
                site = site.format(token=token)
        if segment and token:
            if segment.api_token_place == models.ApiPlaceChoices.PARAM:
                params[segment.api_token_field_name] = token
            elif segment.api_token_place == models.ApiPlaceChoices.HEADER:
                headers[segment.api_token_field_name] = token
            elif segment.api_token_place == models.ApiPlaceChoices.BODY:
                body[segment.api_token_field_name] = token
            elif segment.api_token_place == models.ApiPlaceChoices.LINK:
                site = site.format(token=token)

        try:
            response = request(self.site.method, site, data=body, headers=headers, params=params).json()
            if self.site.name == "coinstats":
                print(self.site.name)
            return response
        except JSONDecodeError as e:
            print(self.site.name, e)
            return {}

    def process_response(self, response):
        scheme = self.site.json_scheme
        obj = self.processor.process(response, scheme)
        segments_loaded = []
        if self.site.first_run:
            segment_list = [[] for i in obj]
            segments_loaded = [False for i in obj]
        else:
            segment_list = []
            for pair in obj:
                if len(models.Pair.objects.filter(site=self.site, token=pair)) == 0:
                    segments = self.parse_segments(pair)
                    segment_list.append(segments)
                    segments_loaded.append(True)
                else:
                    segment_list.append([])
                    segments_loaded.append(False)
        pairs = zip(obj, segment_list, segments_loaded)
        self.save_pairs(pairs)

    def parse_segments(self, pair):
        time.sleep(2)
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
            if self.site.name == 'coinstats':
                print(1)
            self.save_pair(*pair)

    def save_pair(self, pair, segments, segments_loaded):
        if self.site.name == 'coinstats':
            print(pair)
        saved_pair = models.Pair.objects.get_or_create(site=self.site, token=pair)[0]
        saved_pair.segments_loaded = segments_loaded
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
