from django.shortcuts import render
from decouple import config


def index(request):
    context = {
        'ws_url': config('WS_URL'),
    }
    return render(request, 'frontend/index.html', context)
