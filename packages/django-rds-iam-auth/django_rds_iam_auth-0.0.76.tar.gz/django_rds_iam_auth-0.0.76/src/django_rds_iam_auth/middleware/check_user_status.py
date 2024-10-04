import json

from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser


class CheckUserStatusMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if isinstance(request.user, AnonymousUser) or request.user.is_active:
            response = self.get_response(request)
        else:
            response = HttpResponse(
                content=json.dumps({'message': 'Current user is not active'}),
                content_type='application/json',
                status=status.HTTP_403_FORBIDDEN,
            )

        return response
