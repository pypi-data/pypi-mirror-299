import json
from typing import Union

import jwt
import requests
from django.urls import resolve
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse
from django.core.cache import caches

from django_rds_iam_auth.middleware.jwt_exposer import local


class VerifyToken(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name
        if (
                not hasattr(settings, 'NON_SECURE_ROUTES') or url_name not in settings.NON_SECURE_ROUTES and
                not request.path_info.startswith('/admin') and
                not request.path_info.startswith('/manufacture')
        ):
            try:
                self.pre_token_decoding_trigger(request)
                local.access_token_payload = self.decode_token(local.access_token)
                client_id = local.access_token_payload['client_id']
                local.id_token_payload = self.decode_token(local.id_token, client_id)
                local.user_id = local.access_token_payload['sub']
                self.post_token_decoding_trigger(request)
            except jwt.InvalidTokenError as e:
                if e.args[0] == 'Signature verification failed':
                    return self.invalid_token_response()
                elif e.args[0] == 'Signature has expired':
                    return self.token_expire_response()
                elif e.args[0] == 'Invalid payload padding':
                    return self.invalid_padding_response()
                elif e.args[0] == 'Invalid crypto padding':
                    return self.invalid_crypto_padding_response()
                elif e.args[0] in ('Invalid audience', "Audience doesn't match"):
                    return self.invalid_audience_response()
                elif e.args[0] == 'Not enough segments':
                    return self.not_enough_segments()
            except Exception:
                return self.failed_verify_response()
        else:
            local.access_token = None
            local.id_token = None

        response = self.get_response(request)
        return response

    def pre_token_decoding_trigger(self, request):
        pass

    def post_token_decoding_trigger(self, request):
        pass

    @staticmethod
    def cache_jwks_keys():
        all_keys = requests.get(settings.KEYS_URL).json().get('keys')
        if not all_keys:
            raise Exception("Failed to fetch keys")
        for key in all_keys:
            caches['jwk_cache'].set(key['kid'], key, timeout=60 * 60)

    @staticmethod
    def get_jwk(kid: str) -> dict:
        if key := caches['jwk_cache'].get(kid, None):
            return key
        VerifyToken.cache_jwks_keys()
        return caches['jwk_cache'].get(kid, None)

    @staticmethod
    def decode_token(token: str, audience: Union[str, None] = None) -> dict:
        header = jwt.get_unverified_header(token)
        jwk_value = VerifyToken.get_jwk(header['kid'])
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk_value))
        return jwt.decode(token, public_key, audience=audience, algorithms=['RS256'])

    @staticmethod
    def invalid_audience_response():
        return HttpResponse(
            content=json.dumps({'detail': 'Invalid audience'}),
            content_type='application/json',
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def token_expire_response():
        return HttpResponse(
            content=json.dumps({'detail': 'Token expired'}),
            content_type='application/json',
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @staticmethod
    def invalid_padding_response():
        return HttpResponse(
            content=json.dumps({'detail': 'Invalid payload padding'}),
            content_type='application/json',
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def invalid_crypto_padding_response():
        return HttpResponse(
            content=json.dumps({'detail': 'Invalid crypto padding'}),
            content_type='application/json',
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @staticmethod
    def invalid_token_response():
        return HttpResponse(
            content=json.dumps({'detail': 'Invalid token'}),
            content_type='application/json',
            status=status.HTTP_403_FORBIDDEN,
        )

    @staticmethod
    def no_keys_response():
        return HttpResponse(
            content=json.dumps({'details': 'The JWKS endpoint does not contain any keys'}),
            content_type='application/json',
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def access_token_is_missing_response():
        return HttpResponse(
            content=json.dumps({'detail': 'Access token missing'}),
            content_type='application/json',
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def id_token_is_missing_response():
        return HttpResponse(
            content=json.dumps({'details': 'Id token missing'}),
            content_type='application/json',
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def tokens_are_missing_response():
        return HttpResponse(
            content=json.dumps({'details': 'Access and id tokens are missing'}),
            content_type='application/json',
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def not_enough_segments():
        return HttpResponse(
            content=json.dumps({'detail': 'Not enough segments'}),
            content_type='application/json',
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def failed_verify_response():
        return HttpResponse(
            content=json.dumps({'detail': 'Failed to verify token'}),
            content_type='application/json',
            status=status.HTTP_403_FORBIDDEN,
        )
