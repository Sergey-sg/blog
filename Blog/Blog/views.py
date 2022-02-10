from django.http import HttpResponse
from django.shortcuts import render


def page_not_found_view(request, exception) -> HttpResponse:
    """returns a custom page 404"""
    return render(request, '404.html', status=404)
