from __future__ import absolute_import

from django.conf import settings
from datetime import datetime
from os.path import join
from celery import shared_task
from django.db.models import Sum, Count
from django.core.files import File as Fileobj
from django.core.files.storage import FileSystemStorage
from acme_app.models import ProductFile, ProductInfo, ProductWebHook
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import csv
import os
import json
import requests

def stream_file_update(file_id,current_row,total_rows):
	channel_layer = get_channel_layer()
	room = 'file_stream'
	async_to_sync(channel_layer.group_send)(room, {
		"type": "chat.message",
		"room_id": room,
		"message": {"total_rows": total_rows,"current_row":current_row,'file_id': file_id},
	})

@shared_task
def process_file_to_db(file_id):
	try:
		csv_obj = ProductFile.objects.get(id=file_id)
		inserted_rows = 0
		print("Processinggggg")

		f = open(csv_obj.file.path)
		obj = csv.reader(f)
		total_rows = len(list(obj))

		with open(csv_obj.file.path, newline='') as csvfile:
			next(csvfile)
			inserted_rows = 0
			
			filereader = csv.reader(csvfile)
			for row in filereader:
				store, created = ProductInfo.objects.update_or_create(
									sku = row[1],
									defaults={
										'name':row[0], 
										'description': row[2]
									})
				inserted_rows = inserted_rows + 1
				print(inserted_rows)
				stream_file_update(file_id, inserted_rows, total_rows)
			csv_obj.status = 2
			csv_obj.save()
	except:
		csv_obj.status = 3
		csv_obj.save()
		raise


@shared_task
def webhook_event(prod_obj):
	try:
		webhooks = ProductWebHook.objects.all()
		for webhook_obj in webhooks:
			webhook_url = prod_obj.url
			data = {'name': prod_obj.name}
			response = requests.post(
    						webhook_url, data=json.dumps(data),
    						headers={'Content-Type': 'application/json'}
						)
	except:
		pass