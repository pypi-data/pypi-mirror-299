from django.http import HttpResponseForbidden
from .redis_adapter import RedisAdapter
from django.utils.deprecation import MiddlewareMixin


class RateLimitMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.redis_adapter = RedisAdapter()

    def __call__(self, request):
        ip = self.get_client_ip(request)
        self.redis_adapter.set_ip_mask(ip)

        if self.redis_adapter.count_keys(ip) > 100:
            return HttpResponseForbidden("You are blocked due to too many requests.")

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Gets the client IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
