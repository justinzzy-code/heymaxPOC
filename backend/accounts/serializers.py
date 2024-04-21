from rest_framework import serializers
import accounts.models
from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, IntegerField
from django.core.validators import validate_email


class UserRegisterSerializer(ModelSerializer):
    
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    phone_num = serializers.IntegerField(required=True)

    class Meta:
        model = accounts.models.UserModel
        fields =    ["username", "first_name", "last_name", "email", "avatar", "phone_num", "password1", "password2"]

    def validate(self, attrs):
        if len(attrs['password1']) < 8:
            raise serializers.ValidationError("Passwords should be 8 characters long")
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords not the same!")
        if accounts.models.UserModel.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("This username has already been used")
        if attrs['email']:
            try:
                validate_email(attrs['email'])
            except:
                raise serializers.ValidationError("Email is not valid")
        return attrs

    def create(self, validated_data):
        if 'avatar' not in validated_data:
            user = accounts.models.UserModel.objects.create_user(username=validated_data['username'],
                                               first_name=validated_data['first_name'],
                                               last_name=validated_data['last_name'],
                                               email=validated_data['email'],
                                               phone_num=validated_data['phone_num'])
        else:
            user = accounts.models.UserModel.objects.create_user(username=validated_data['username'],
                                               first_name=validated_data['first_name'],
                                               last_name=validated_data['last_name'],
                                               email=validated_data['email'],
                                               phone_num=validated_data['phone_num'],
                                               avatar = validated_data['avatar'])
        user.set_password(validated_data['password1'])
        user.save()

        return user
    
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = accounts.models.UserModel
        fields = ["username", "first_name", "last_name", "email", "avatar", "phone_num"]

class UserProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = accounts.models.UserModel
        fields = ["username", "first_name", "last_name", "email", "avatar", "phone_num"]