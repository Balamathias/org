from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Organization, User


class InterfaceTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token
    

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'firstName', 'lastName', 'phone', 'password', 'password2', 'userId')
        extra_kwargs = {
            'firstName': {'required': True},
            'lastName': {'required': True},
            'phone': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone=validated_data['phone'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName']
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['userId', 'email', 'firstName', 'lastName', 'password', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['orgId', 'name', 'description']
        