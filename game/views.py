from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SpinRequestSerializer, SpinResponseSerializer
from .utils import spin_slot_machine_logic
from rest_framework import generics
from rest_framework.permissions import AllowAny
from knox.models import AuthToken
from .models import CustomUser
from rest_framework import generics, permissions
from knox.models import AuthToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "money": user.money,
            },
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extract username and password from validated data
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Perform authentication
        user = authenticate(username=username, password=password)
        
        if user:
            # If user is authenticated, generate token
            _, token = AuthToken.objects.create(user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token
            })
        else:
            return Response({
                "error": "Invalid credentials"
            }, status=status.HTTP_400_BAD_REQUEST)


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
class SpinSlotMachineView(APIView):
    def post(self, request):
        serializer = SpinRequestSerializer(data=request.data)
        if serializer.is_valid():
            initial_money = serializer.validated_data['initial_money']
            stavka = serializer.validated_data['stavka']
            result = spin_slot_machine_logic(initial_money, stavka)
            response_serializer = SpinResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
