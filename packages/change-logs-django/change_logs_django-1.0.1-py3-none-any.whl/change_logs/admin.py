from django.contrib import admin
from django.utils.html import format_html

from change_logs.models import ChangeLog, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag Admin."""

    list_display = ('name', 'color',)
    search_fields = ('name',)

    def color(self, obj):
        return format_html('<span style="color: {};">{}</span>', obj.color_hex, obj.color_hex)


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    """ChangeLog Admin."""

    list_display = ('title', 'version', 'author', 'date',)
    search_fields = ('title', 'version', 'tags__name')
    list_filter = ('author', 'date', 'tags',)
