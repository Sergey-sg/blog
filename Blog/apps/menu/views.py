from django.views.generic import ListView

from .constants import Position, Target
from .models import Menu


class MenuHeader(ListView):

    template_name = 'menu/header.jinja2'

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = Menu.objects.filter(position=Position.HEADER, show_item=True)
        self_item = queryset.filter(target=Target.SELF)
        partner = queryset.filter(target=Target.BLANK)
        return {'self_items': self_item, 'partner': partner}
