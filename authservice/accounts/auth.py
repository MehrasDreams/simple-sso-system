from datetime import datetime, timedelta
from rest_framework import serializers
from .models import UsersToken

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)  # clean the token

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        # Get the user from the database
        username_or_phone_number = payload.get('user_identifier')
        if username_or_phone_number is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(phone=username_or_phone_number).first()
        if user is None:
            user = User.objects.filter(phone=username_or_phone_number).first()
            if user is None:
                raise AuthenticationFailed('User not found')

        # Return the user and token payload
        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user):
        # Create the JWT payload
        payload = {
            'user_identifier': user.phone,
            'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONF.get("TOKEN_LIFETIME_HOURS"))).timestamp()),
            # set the expiration time for 5 hour from now
            'iat': datetime.now().timestamp(),
            'phone_number': user.phone
        }

        # Encode the JWT with your secret key
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        # Save token on database

        try:
            get_user = User.objects.get(phone=user)
            get_token = UsersToken.objects.get(user=get_user.id)
            token = get_token.token

        except UsersToken.DoesNotExist:
            get_or_create_token = UsersToken.objects.create(user=str(get_user.id), token=jwt_token)
            token = get_or_create_token.token

        return token

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token




class ObtainTokenSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=False, allow_null=False)


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(allow_null=False, allow_blank=False)
