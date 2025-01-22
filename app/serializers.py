from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from app.models import Content

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["role"]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password")
        token, created = Token.objects.get_or_create(user=user)
        data["token"] = token
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ['user']


class ContentDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Content
        fields = '__all__'
