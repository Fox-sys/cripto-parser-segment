# Generated by Django 4.2.1 on 2023-06-30 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0008_pair_segments_loaded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pair',
            name='segments_loaded',
            field=models.BooleanField(default=False, verbose_name='Сегменты загружены'),
        ),
        migrations.AlterField(
            model_name='segment',
            name='api_token_place',
            field=models.CharField(choices=[('header', 'header'), ('body', 'body'), ('param', 'param'), ('link', 'link')], max_length=10, verbose_name='Место где хранится токен'),
        ),
        migrations.AlterField(
            model_name='site',
            name='api_key_place',
            field=models.CharField(choices=[('header', 'header'), ('body', 'body'), ('param', 'param'), ('link', 'link')], max_length=10, verbose_name='Место где хранится ключ'),
        ),
    ]