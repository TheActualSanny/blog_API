from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class Register(APIView):
    def get(self, request):
        return Response({
            'message' : 'Please pass the account credentials!'
        })

    def post(self, request):
        account_serializer = RegisterSerializer(data = request.data)
        if not account_serializer.is_valid():
            raise ValidationError(account_serializer.errors)
        username = account_serializer.validated_data.get('username')
        password = account_serializer.validated_data.get('password')
        user = User.objects.create_user(username = username, password = password)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message' : 'Account created successfully!',
            'access' : str(refresh.access_token),
            'refresh' : str(refresh)
        })
    

class Login(APIView):
    def get(self, request):
        return Response({
            'message' : 'Please pass the account credentials!'
        })

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if authenticate(username = username, password = password):
            current_user = User.objects.get(username = username)
            refresh = RefreshToken.for_user(current_user)
            return Response({
                'message' : 'Successfully logged in!',
                'access' : str(refresh.access_token),
                'refresh' : str(refresh)
            })
        else:
            raise AuthenticationFailed('Make sure to pass correct credentials!')

class Logout(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass
