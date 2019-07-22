from rest_framework import serializers
from authentication_app.models import User
from acme_app.models import ProductFile, ProductInfo
from django.contrib.auth import get_user_model
from tempfile import mkdtemp
from acme_project.helper import form_error_to_list, get_file_mime_type
from django.core.files import base
from django.conf import settings
import os


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name','email')

class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, allow_null=False)
    
    class Meta:
        model = ProductFile
        fields = ['file']

    def validate(self,attrs):
        super(AttachmentSerializer, self).validate(self)
        if 'file' not in attrs:
            raise serializers.ValidationError('No file found')
        try:
            fp_uploaded_file = base.File(attrs['file'])
            fp_uploaded_file.seek(0)
            file_mime = get_file_mime_type(fp_uploaded_file)
            if file_mime in settings.ATTACHMENT_SUPPORTED_FILE_FORMATS.keys():
                if self.cleaned_data['file'].size > settings.ATTACHMENT_MAX_FILE_UPLOAD_SIZE:
                    raise serializers.ValidationError('The File size must not exceed {} bytes.'.format(settings.ATTACHMENT_MAX_FILE_UPLOAD_SIZE))
            else:
                raise serializers.ValidationError('This File type ({}) is not supported.'.format(file_mime))
        except AttributeError:
            pass
        
        return attrs


class  FetchFileSerializer(serializers.ModelSerializer):
    created_by = UsersSerializer(required=True, allow_null=False)
    file = serializers.FileField(required=True, allow_null=False)

    class Meta:
        model = ProductFile
        fields = ('file','created_by','status')
        related_object = 'created_by'

class FetchProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ('name','sku','description','status','created_date')


class CreateProductSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True, allow_null=False,max_length = 250)
    sku = serializers.CharField(required=True, allow_null=False, max_length = 250)
    description = serializers.CharField(required=False, allow_null=True)
    status = serializers.IntegerField(max_value=2, min_value=1)

    class Meta:
        model = ProductInfo
        fields = ('name','sku','description','status')

    def create(self, validated_data):
        product, created = ProductInfo.objects.update_or_create(
                            name = validate_data['name'],
                            sku = validate_data['sku'], 
                            description = validate_data['description'],
                            status = validate_data['status']
                        )
        return product

