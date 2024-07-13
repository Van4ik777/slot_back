from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'money')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'money')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            money=1000  
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")
    
class SpinRequestSerializer(serializers.Serializer):
    initial_money = serializers.IntegerField()
    stavka = serializers.IntegerField()


class SpinResponseSerializer(serializers.Serializer):
    l1 = serializers.ListField()
    l2 = serializers.ListField()
    l3 = serializers.ListField()
    money = serializers.IntegerField()
    winning_lines = serializers.ListField()
    multiplier = serializers.FloatField()
    message = serializers.CharField(required=False)
