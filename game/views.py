from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, SpinRequestSerializer, SpinResponseSerializer
from .utils import spin_slot_machine_logic

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        access_token = AuthToken.objects.create(user)[1]
        refresh_token = RefreshToken.for_user(user)
        response = JsonResponse({
            "user": {
                "id": user.id,
                "username": user.username,
                "money": user.money,
            },
            "token": access_token,
            "refresh_token": str(refresh_token),
        })
        response.set_cookie(key='access_token', value=access_token, httponly=True, samesite='Lax')
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, samesite='Lax')
        return response

class LoginAPI(KnoxLoginView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        access_token = AuthToken.objects.create(user)[1]
        refresh_token = RefreshToken.for_user(user)
        response = JsonResponse({
            "user": UserSerializer(user).data,
            "token": access_token,
            "refresh_token": str(refresh_token),
        })
        response.set_cookie(key='access_token', value=access_token, httponly=True, samesite='Lax')
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, samesite='Lax')
        return response

class RefreshAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
                user = refresh_token.user
                access_token = AuthToken.objects.create(user)[1]
                response = JsonResponse({
                    "token": access_token,
                })
                response.set_cookie(key='access_token', value=access_token, httponly=True, samesite='Lax')
                return response
            except TokenError as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

class UserAPI(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class SpinSlotMachineView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = SpinRequestSerializer(data=request.data)
        if serializer.is_valid():
            initial_money = serializer.validated_data['initial_money']
            stavka = serializer.validated_data['stavka']
            result = spin_slot_machine_logic(initial_money, stavka)
            user = request.user 
            user.money = result['money']  
            user.save()  
            response_serializer = SpinResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)