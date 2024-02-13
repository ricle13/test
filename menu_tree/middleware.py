from django.http import Http404
from django.shortcuts import redirect
from .models import MenuItem

class MenuMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/admin/'):
            path = request.path.strip('/')
            if path:
                try:
                    MenuItem.objects.get(url=path)
                except MenuItem.DoesNotExist:
                    raise Http404("Страница не найдена")
        return self.get_response(request)