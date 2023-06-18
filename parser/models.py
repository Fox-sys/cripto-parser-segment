from django.db import models


class ApiPlaceChoices:
    HEADER = 'header'
    BODY = 'body'
    LINK = 'link'

    @classmethod
    def get_choices(cls):
        return [('header', 'header'), ('body', 'body'), ('link', 'link')]


class Site(models.Model):
    name = models.CharField('Название сайта', max_length=150)
    is_active = models.BooleanField('Активен', default=True)
    list_api_link = models.URLField('Ссылка на список')
    json_scheme = models.TextField('Схема обработки ответов')
    api_key = models.CharField('Апи ключ', max_length=100)
    api_key_field_name = models.CharField('Название поля для api ключа', max_length=100)
    api_key_place = models.CharField('Место где хранится ключ', max_length=10, choices=ApiPlaceChoices.get_choices())
    first_run = models.BooleanField('Первый запуск', default=True)
    link_template = models.CharField('Шаблон ссылки', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Сайт'
        verbose_name_plural = 'Сайты'

    def __str__(self):
        return self.name


class Segment(models.Model):
    json_name = models.CharField('Название json поля', max_length=20)
    api_link = models.URLField('Ссылка на сегмент')
    is_active = models.BooleanField('Активен', default=True)
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    api_token_place = models.CharField('Место где хранится токен', max_length=10, choices=ApiPlaceChoices.get_choices())
    api_token_field_name = models.CharField('Название токена', max_length=100, blank=True)
    json_scheme = models.TextField('Схема обработки ответов')
    scheme_single_target_mode = models.BooleanField('Single target mode', default=True)

    class Meta:
        verbose_name = 'Сегмент'
        verbose_name_plural = 'Сегменты'


class Pair(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    token = models.CharField('Индивидуальный токен валюты', max_length=100)
    sent = models.BooleanField('отправленно', default=False)
    segments_loaded = models.BooleanField('Сегменты загружены', default=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Пара'
        verbose_name_plural = 'Пары'
        unique_together = [('site', 'token')]


class PairSegment(models.Model):
    json_name = models.CharField('Название json поля', max_length=20)
    content = models.TextField('json контент', blank=True)
    pair = models.ForeignKey('Pair', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сегмент пары'
        verbose_name_plural = 'Сегменты пары'
        unique_together = [('json_name', 'pair')]


class Bot(models.Model):
    chat_id = models.CharField('Id чата', max_length=50)
    bot_token = models.CharField('Токен Бота', max_length=150)

    def __str__(self):
        return self.chat_id

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'
