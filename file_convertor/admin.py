from django.contrib import admin
from .models import TxtToJson


@admin.register(TxtToJson)
class PairAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    readonly_fields = ('output_file_download', )
    search_fields = ('id',)
    exclude = ('output_file',)
