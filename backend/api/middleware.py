from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token


class DisableCSRFForAPI(MiddlewareMixin):
    """Отключает CSRF для API endpoints"""
    
    def process_request(self, request):
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None

