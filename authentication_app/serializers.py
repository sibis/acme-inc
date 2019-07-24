from rest_framework import serializers
from authentication_app.models import User
from django.contrib import auth
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def create(self, validated_data):
        user = UserModel.objects.create(email = validated_data['email'], name=validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
    	model = User
    	fields = ('email', 'password')

    def clean(self):
    	super(LoginSerializer, self).clean()

    	if self.cleaned_data.get('email',None) is not None and self.cleaned_data.get('password',None) is not None:
    		user = auth.authenticate(email=self.cleaned_data['email'], password=self.cleaned_data['password'])
    		if user is None:
    			raise serializers.ValidationError("Invalid Username or Password!")
    			
    		return self.cleaned_data