from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from.models import Menu


@admin.register(Menu)
class MenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'item_url', 'target', 'position', 'show_item', ]
    list_filter = ['position', 'show_item']
