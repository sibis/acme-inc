from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from authentication_app.serializers import UserSerializer, LoginSerializer
from authentication_app.models import User
from authentication_app.backends import EmailAuthBackend

from rest_framework.decorators import api_view, permission_classes
from rest_framework import authentication, permissions, status
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
	print("sibi")
	serialized = UserSerializer(data=request.data)
	if serialized.is_valid():
		serialized.save()
		return Response(serialized.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login_test(request):
	serialized = LoginSerializer(data=request.data)
	if serialized.is_valid():
		user = authenticate(username=serialized.data['email'], password=serialized.data['password'])
		if user is not None :
			auth.login(request, user)
			return Response(request.user, status=status.HTTP_200_OK)
		else:
			return Response(serialized._errors, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
	username = request.data.get("username")
	password = request.data.get("password")
	if username is None or password is None:
		return Response({'error': 'Please provide both username and password'},
					status=HTTP_400_BAD_REQUEST)
	user = EmailAuthBackend.authenticate(username=username, password=password)
	if not user:
		return Response({'error': 'Invalid Credentials'},
					status=HTTP_404_NOT_FOUND)
	token,_ = Token.objects.get_or_create(user=user)
	return Response({'token': token.key,'email':user.email,'user_id':user.id},
					status=HTTP_200_OK)


@csrf_exempt
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def logout(request):
	request.user.auth_token.delete()
	return Response({'msg': 'Successfully logged out!'},status=status.HTTP_200_OK)
