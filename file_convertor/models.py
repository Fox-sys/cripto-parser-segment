from django.db import models
from django.conf import settings
from project.file_savers.file_convertor.txt_to_json import txt_to_json_file_saver
import json


class TxtToJson(models.Model):
    input_file = models.FileField(upload_to=txt_to_json_file_saver)
    output_file = models.FileField(upload_to=txt_to_json_file_saver, blank=True, null=True)

    def __str__(self):
        return f'конвертация №{self.id}'

    class Meta:
        verbose_name = 'Txt -> json'
        verbose_name_plural = 'Txt -> json'

    def save(self, **kwargs):
        super().save(**kwargs)
        with open(settings.BASE_DIR / 'media' / self.input_file.path) as file:
            data = [i.split(', ') for i in file.read().split('\n')]
        output = []
        for elem in data:
            try:
                output.append({'name': elem[0], 'link': '', 'telegram_link': elem[1]})
            except:
                pass
        output_path = txt_to_json_file_saver(self, self.input_file.path.split('/')[-1] + '.json')
        print(output_path)
        with open(settings.BASE_DIR / 'media' / output_path, 'w') as file:
            json.dump(output, file)
        self.output_file = output_path
        return super().save(**kwargs)
