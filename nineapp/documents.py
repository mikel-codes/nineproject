# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django_elasticsearch_dsl import DocType, Index, fields
from django.contrib.auth.models import User
from .models import Post, Category




# Name of the Elasticsearch index
search_index = Index('library')
# See Elasticsearch Indices API reference for available settings
search_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@search_index.doc_type
class PostDocument(DocType):
	class Meta:
		model  = Post
		fields = ('topic', 'tags', 'post_by')
		related_models = ('Category', 'User')
