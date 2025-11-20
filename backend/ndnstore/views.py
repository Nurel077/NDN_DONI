from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    """Главная страница сайта"""
    return render(request, 'index.html')

def api_info(request):
    """Информация об API"""
    return JsonResponse({
        'message': 'NDN Store API',
        'version': '1.0',
        'endpoints': {
            'register': '/api/register/',
            'login': '/api/login/',
            'logout': '/api/logout/',
            'profile': '/api/profile/',
            'settings': '/api/settings/',
            'games': '/api/games/',
            'admin': '/admin/',
        }
    })

