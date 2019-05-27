#gcloud.py

#-*- coding:utf-8 -*-

from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage



class GsPostCloud(GoogleCloudStorage):
	location = "media/posts/photos"
	file_overwrite=True
	file_max_size = settings.MAX_IMG_SIZE

class GsStaticCloud(GoogleCloudStorage):
	location="static"
	

class GsPictureProfileCloud(GoogleCloudStorage):
	location = "media/profiles/pics"
	file_overwrite = True
	file_max_size = settings.MAX_IMG_SIZE



