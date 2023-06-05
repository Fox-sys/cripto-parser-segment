# Generated by Django 4.2.1 on 2023-06-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0002_pair_json_scheme'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pair',
            name='json_scheme',
        ),
        migrations.AddField(
            model_name='site',
            name='json_scheme',
            field=models.TextField(default='', verbose_name='Схема обработки ответов'),
            preserve_default=False,
        ),
    ]
