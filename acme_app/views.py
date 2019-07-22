from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from acme_app.serializers import AttachmentSerializer, FetchFileSerializer
from acme_project.helper import form_error_to_list, get_file_mime_type
from acme_app.tasks import process_file_to_db
from django.contrib.auth import get_user_model
from acme_app.models import ProductFile
from authentication_app.models import User
from shutil import copyfileobj
from tempfile import mkdtemp
from wsgiref.util import FileWrapper
import csv


@csrf_exempt
@api_view(['POST']) 
@permission_classes((permissions.IsAuthenticated,))
def upload_file(request):
	"""
    Function to upload the file
    params: file and file type to be passed  (refer models)
    NOTE: File needs to meet the required creiteria (settings.ATTACHMENT*) to be accepted 
    """
	file_form = AttachmentSerializer(data = request.data)
	if file_form.is_valid():
		files = request.FILES
		for file in files.values():
	 		file_obj = ProductFile.objects.create(file=file,created_by=request.user)
	 		process_file_to_db.delay(file_obj.id)
	 		return Response(file_form.data, status=status.HTTP_201_CREATED)
	else:	 	
		return Response(file_form._errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET']) 
@permission_classes((permissions.IsAuthenticated,))
def get_uploaded_file_status(request):
	"""
    The uploaded files lists with created user info and date time
    """
	try:
		file_obj = FetchFileSerializer(File.objects.filter(created_by=request.user).order_by('-created_on'), many=True)
		return Response({'msg':'Files retrived successfully!', 'data':file_obj.data},status = status.HTTP_200_OK)
	except Exception as e:
		return Response({'msg':str(e)}, status=status.HTTP_404_NOT_FOUND)
