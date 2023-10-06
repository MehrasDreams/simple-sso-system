from django.contrib.auth import get_user_model
from rest_framework import views, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UsersToken, Profile
from utils.otp import OTP_MANAGER
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .auth import JWTAuthentication, ObtainTokenSerializer, TokenSerializer, \
    SendCodeSerializer

# TODO: fix the import bug
User = get_user_model()

from .serializers import UserDetailSerializer, UpdateUserSerializer


class ObtainTokenView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_phone_number = serializer.validated_data.get('phone')
        code = serializer.validated_data.get('code')
        jwt_token = {}

        otp_checker = OTP_MANAGER.otp_checker(phone=username_or_phone_number, code=code)

        if otp_checker:
            user = User.objects.filter(phone=username_or_phone_number).first()
            if user is None:
                new_user = User.objects.create(phone=username_or_phone_number)
                jwt_token = JWTAuthentication.create_jwt(new_user)


            # if user is None or not user.check_password(code):
            #     return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate the JWT token

            elif user is not None:

                jwt_token = JWTAuthentication.create_jwt(user)
            OTP_MANAGER.remove_code(phone=username_or_phone_number)
            return Response({'token': jwt_token})

        else:

            return Response({'error': 'Invalid information'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyApiView(views.APIView):
    permissions = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        response = {}
        if serializer.is_valid():
            try:
                get_token = UsersToken.objects.get(token=serializer.data['token'])

                return Response({"data": get_token.id}, status=status.HTTP_200_OK)
            except UsersToken.DoesNotExist:
                return Response({"data": "Is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SendCode(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SendCodeSerializer(data=request.data, many=False)

        if serializer.is_valid():
            response = OTP_MANAGER.create_otp_code(phone=serializer.data['phone'])
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        get_user = Profile.objects.get(phone=request.user)
        serializer = UserDetailSerializer(instance=get_user, many=False)

        return Response({'user': serializer.data})
