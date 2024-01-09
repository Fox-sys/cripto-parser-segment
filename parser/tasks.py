import json
import time
import traceback

from project import celery_app
from .models import Site, Pair, Bot
from parser.core.parser import Parser
from parser.core.send_file import send_file, send_new
import re


@celery_app.task
def parse_shift():
    bot = Bot.objects.first()
    for site in Site.objects.filter(is_active=True):
        try:
            parser = Parser(site)
            parser.parse_site()
        except (KeyError, ValueError):
            content = f'Обнаружена проблема с api сайта {site.name}, желательно проверить ссылку и схему парсинга'
            print(traceback.format_exc())
            send_new(bot.bot_token, bot.chat_id, content)
        except Exception:
            content = f'Что то поломалось, время звать Бориса (сайт: {site.name})'
            print(traceback.format_exc())
            send_new(bot.bot_token, bot.chat_id, content)
    send_pairs('Новые%20пары')


@celery_app.task
def parse_segment_unloaded():
    sites = Site.objects.all()
    for site in sites:
        parser = Parser(site)
        pairs = Pair.objects.filter(segments_loaded=False, site=site).values_list('token', flat=True)[:40]
        print(pairs)
        segments = []
        for pair in pairs:
            segments_pair = parser.parse_segments(pair)
            segments.append(segments_pair)
            time.sleep(2)
        saving_pairs = zip(pairs, segments, [True for i in range(40)])
        parser.save_pairs(saving_pairs)
    send_pairs('Старые%20пары')


def send_pairs(title):
    js = []
    pairs = Pair.objects.filter(sent=False)
    if len(pairs) <= 15:
        return
    bot = Bot.objects.first()
    for pair in pairs:
        js_pair = {'name': pair.token}
        if pair.site.link_template:
            link_template = pair.site.link_template.replace('{token}', pair.token)
            camps = re.findall(r'{[a-zA-Z]+}', link_template)
            for camp in camps:
                try:
                    segment = pair.pairsegment_set.get(json_name=camp[1:-1])
                except:
                    continue
                link_template = link_template.replace(camp, json.loads(segment.content))
            js_pair['link'] = link_template
        for segment in pair.pairsegment_set.all():
            js_pair[segment.json_name] = json.loads(segment.content)
        js.append(js_pair)
        pair.sent = True
        pair.save()
    links = []
    result = []
    for obj in js:
        try:
            if isinstance(obj['telegram_link'], list):
                for link in obj['telegram_link']:
                    if 't.me' in link:
                        obj['telegram_link'] = link
                        break
            if not ('t.me' in obj['telegram_link']):
                obj['telegram_link'] = f'https://t.me/{obj["telegram_link"]}'
            if not (obj['telegram_link'] in links):
                result.append(obj)
                links.append(obj['telegram_link'])
        except:
            ...
    send_file(title, bot.bot_token, bot.chat_id, json.dumps(js, indent=1))
