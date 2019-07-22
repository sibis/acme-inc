from __future__ import absolute_import

from django.conf import settings
from datetime import datetime
from os.path import join
from celery import shared_task
from django.db.models import Sum, Count
from django.core.files import File as Fileobj
from django.core.files.storage import FileSystemStorage
from acme_app.models import ProductFile, ProductInfo
import csv
import os
import json

def stream_file_update(file_id,current_row,total_tows):
	message['current_row'] = current_row
	message['total_tows'] = total_tows
	message['file_id'] = file_id
	channel_layer = get_channel_layer()
	room = 'file_stream'
	async_to_sync(channel_layer.group_send)(room, {
		"type": "chat.message",
		"room_id": room,
		"message": {"activity": 'file_stream',"data":message},
	})

@shared_task
def process_file_to_db(file_id):
	try:
		csv_obj = ProductFile.objects.get(id=file_id)
		inserted_rows = 0
		with open(csv_obj.file.path, newline='') as csvfile:
			next(csvfile)
			filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			data = list(filereader)
			total_tows = len(data)
			for row in filereader:
				data = row[0].split(",")
				store, created = ProductInfo.objects.update_or_create(
									name = data[0],
									sku = data[1], 
									description = data[2]
								)
				inserted_rows = inserted_rows + 1
				stream_file_update(file_id, inserted_rows, total_tows)
		csv_obj.status = 2
		csv_obj.save()
	except:
		csv_obj.status = 3
		csv_obj.save()
		raise
