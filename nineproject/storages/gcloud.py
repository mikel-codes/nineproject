#gcloud.py

#-*- coding:utf-8 -*-

from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from urllib.parse import urljoin

class GsPostCloud(GoogleCloudStorage):
	location = "media/posts/photos"
	file_overwrite=False

class GsStaticCloud(GoogleCloudStorage):
	location="static"


class GsPictureProfileCloud(GoogleCloudStorage):
	location="media/profiles/pics"
	file_overwrite = True

class GsThumbnailProfileCloud(GoogleCloudStorage):
	location="media/profiles/thumbs"
	file_overwrite = True

