from typing import Any
from django.shortcuts import render

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.views import APIView

from .serializers import OrganizationSerializer, RegisterSerializer, TokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view

from interface.models import Organization, User


class ObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = {
                'message': 'Registration successful',
                'status': 'success',
                'data': {
                    'user': serializer.data,
                    'accessToken': access_token,
                    'refreshToken': refresh_token
                }
            }
            return Response(response, status=status.HTTP_201_CREATED, headers=headers)
        
        except ValidationError as e:
            error_response = {
                'status': 'Bad request',
                'message': 'Registration unsuccessful',
                'statusCode': 400,
                'errors': e.detail
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_detail(request: Any, userId: str) -> Any:
    user = User.objects.get(userId=userId)
    serializer = UserSerializer(user)
    data = serializer.data
    print(data)

    response = {
        'status': 'success',
        'message': 'User details retrieved successfully',
        'data': data
    }
    return Response(response, status=status.HTTP_200_OK)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'userId'
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user_data = serializer.data

        custom_response = {
            'status': 'success',
            'message': 'User details retrieved successfully',
            'data': user_data
        }
        return Response(custom_response, status=status.HTTP_200_OK)


class CreateOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            organization = serializer.save()
            request.user.organization = organization
            request.user.save()

            return Response(
                {
                    'status': 'success', 
                    'message': 'Organization created successfully', 
                    'organization': serializer.data
                }, 
                status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {
                    'status': 'error', 
                    'message': 'Organization creation failed', 
                    'errors': serializer.errors
                 }, 
                status=status.HTTP_400_BAD_REQUEST)
        

class OrganizationListView(ListCreateAPIView):
    model = Organization
    permission_classes = [IsAuthenticated]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        org_data = serializer.data
        return Response({
            'status': 'success',
            'message': 'Retrieved organisations successfully',
            'data': {
                'organisations': org_data
            }
        }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            org = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            response = {
                'message': 'Creation of Organisation successful',
                'status': 'success',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED, headers=headers)
        
        except ValidationError as e:
            error_response = {
                'status': 'Bad request',
                'message': 'Creation of Organisation unsuccessful',
                'statusCode': 400,
                'errors': e.detail
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        org = serializer.save()
        self.request.user.organization = org
        self.request.user.save()
        return org
    

class RetrieveOrganisationView(RetrieveAPIView):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = 'orgId'
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        org_data = serializer.data

        custom_response = {
            'status': 'success',
            'message': 'Organisation details retrieved successfully',
            'data': org_data
        }
        return Response(custom_response, status=status.HTTP_200_OK)
    

class AddUserToOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, orgId, *args, **kwargs):
        user_id = request.data.get('userId')
        if not user_id:
            return Response({
                'status': 'error',
                'message': 'User ID is required',
                'statusCode': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(userId=user_id)
            organization = Organization.objects.get(orgId=orgId)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found',
                'statusCode': 404
            }, status=status.HTTP_404_NOT_FOUND)
        except Organization.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Organization not found',
                'statusCode': 404
            }, status=status.HTTP_404_NOT_FOUND)

        user.organization = organization
        user.save()

        return Response({
            'status': 'success',
            'message': 'User added to organisation successfully'
        }, status=status.HTTP_200_OK)
