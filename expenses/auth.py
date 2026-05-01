from functools import wraps
from django.http import JsonResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from .models import User


def google_auth(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else ''
        if not token:
            return JsonResponse({'error': 'No token'}, status=401)

        # Email-based user token (starts with email_)
        if token.startswith('email_'):
            try:
                user = User.objects.get(google_id=token)
                request.guser = user
                return view_func(request, *args, **kwargs)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Invalid token'}, status=401)

        # Google ID token
        try:
            payload = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
            user, _ = User.objects.update_or_create(
                google_id=payload['sub'],
                defaults={'email': payload.get('email', ''), 'name': payload.get('name', ''), 'picture': payload.get('picture', '')}
            )
            request.guser = user
        except Exception:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
