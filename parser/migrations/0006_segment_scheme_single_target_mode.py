# Generated by Django 4.2.1 on 2023-06-04 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0005_segment_api_token_field_name_segment_api_token_place_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='segment',
            name='scheme_single_target_mode',
            field=models.BooleanField(default=True, verbose_name='Single target mode'),
        ),
    ]
