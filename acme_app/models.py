from django.db import models
from authentication_app.models import User
from django.conf import settings
import os

def file_attachment_path(instance, filename):
	return os.path.join(settings.ATTACHMENTS_DIR_NAME, filename)

class ProductFile(models.Model):

	PENDING = 1
	SUCCESS = 2
	ERROR = 3

	__file_sync_status = (
		(PENDING,'Pending'),
		(SUCCESS, 'Success'),
		(ERROR,'Error')
	)

	file = models.FileField(upload_to = file_attachment_path)
	status = models.SmallIntegerField(choices = __file_sync_status, default = PENDING)
	created_by = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'created_by')
	created_on = models.DateTimeField(auto_now = True)

	def filename(self):
		return os.path.basename(self.file.name)


class ProductInfo(models.Model):
	name = models.CharField(max_length = 250)
	sku = models.CharField(max_length = 250, unique = True, db_index = True)
	description = models.TextField(null = True)
	created_date = models.DateTimeField(auto_now_add = True)
	modified_date = models.DateTimeField(auto_now = True)
