from django.db import models
from authentication_app.models import User
from django.conf import settings
import os


def file_attachment_path(filename):
	return os.path.join(settings.ATTACHMENTS_DIR_NAME, filename)


class ProductFile(models.Model):

	PENDING = 1
	SUCCESS = 2
	ERROR = 3

	__file_sync_status = (
		(PENDING, 'Pending'),
		(SUCCESS, 'Success'),
		(ERROR, 'Error')
	)

	file = models.FileField(upload_to=file_attachment_path)
	status = models.SmallIntegerField(choices=__file_sync_status, default=PENDING)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='created_by')
	created_date = models.DateTimeField(auto_now=True)

	def filename(self):
		return os.path.basename(self.file.name)


class ProductInfo(models.Model):

	ACTIVE = 1
	INACTIVE = 2

	__product_status = (
		(ACTIVE, 'Active'),
		(INACTIVE, 'Inactive')
	)

	name = models.CharField(max_length=240)
	sku = models.CharField(max_length=240, unique=True, db_index=True)
	description = models.TextField(null=True)
	status = models.SmallIntegerField(choices=__product_status, default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)


class ProductWebHook(models.Model):

	MANUAL_TRIGGER = 1
	UPLOAD_TRIGGER = 2

	__webhook_event_status = (
		(MANUAL_TRIGGER, 'Manual Trigger'),
		(UPLOAD_TRIGGER, 'Upload Trigger')
	)

	name = models.CharField(max_length=50)
	url = models.URLField(max_length=300)
	event = models.SmallIntegerField(choices=__webhook_event_status, default=MANUAL_TRIGGER)
	active = models.BooleanField(default=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='creator')
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
