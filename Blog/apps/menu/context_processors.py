from .models import Menu


def access_menu_items(request):
    """
      The context processor return a dictionary og menu item.
    """
    menu_items = Menu.objects.filter(show_item=True)
    return {'menu_items': menu_items}

