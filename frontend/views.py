from django.shortcuts import render
from decouple import config


def index(request):
    context = {
        'ws_url': config('WS_URL'),
        'icon_url': config('ICON_URL'),
    }
    return render(request, 'frontend/index.html', context)
