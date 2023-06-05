from django.contrib import admin
from parser import models


@admin.action(description="Пометить как отправленные")
def make_sent(model_admin, request, queryset):
    queryset.update(sent=True)


@admin.action(description="Пометить как не отправленные")
def make_unsent(model_admin, request, queryset):
    queryset.update(sent=False)


@admin.action(description="Пометить как активные")
def make_active(model_admin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Пометить как не активные")
def make_inactive(model_admin, request, queryset):
    queryset.update(is_active=False)


class SegmentInline(admin.StackedInline):
    model = models.Segment
    extra = 1


class PairSegmentInline(admin.StackedInline):
    model = models.PairSegment
    extra = 0


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active')
    list_filter = ('is_active',)
    inlines = [SegmentInline]
    actions = (make_active, make_inactive)


@admin.register(models.Pair)
class PairAdmin(admin.ModelAdmin):
    list_display = ('token', 'site', 'sent')
    readonly_fields = ('site', 'token', 'sent')
    list_filter = ('site', 'sent')
    search_fields = ('token',)
    actions = (make_sent, make_unsent)
    inlines = [PairSegmentInline]


@admin.register(models.Bot)
class ParseTimeAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
