# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys, os
from io import StringIO, BytesIO

from PIL import Image
from pathlib import Path
import requests
from urllib.request import urlopen
from django.db import models
from django.contrib.auth.models import  User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from django.core.files.storage import default_storage as storage
##from django.contrib.postgres.fields import ArrayField
from django.core.files.base import ContentFile
from django.utils.encoding import python_2_unicode_compatible
from utils.modelmixins import TimeMixin, MetaTagsMixin
from tinymce.models import HTMLField
#from django.contrib.gis.utils import GeoIP
from django.contrib.auth.models import Group

from nineproject.storages.gcloud import GsPictureProfileCloud as gppc, GsPostCloud as gpostc
# Create your models here.



@python_2_unicode_compatible
class Profile(TimeMixin):
    ROLES = (
        (1, 'blogger'),
        (2, 'superblogger'),
        (3, ''),
        )
    
    author = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio    = models.TextField(_("Describe Yourself"), max_length=200,error_messages = {'max_length': "Exceed limit of 200 characters)"}, default="I am a blogger")
    role   = models.PositiveSmallIntegerField(choices=ROLES, default=1, null=True, blank=True)
    ip_addr  = models.GenericIPAddressField(protocol="ipv4", null=True, blank=True)
    location = models.CharField(_("blogger's country"), max_length=30, blank=True)
    picture  = models.ImageField(storage=gppc(), null=True, blank=True)


    def __str__(self):
        return self.author.get_full_name()




@python_2_unicode_compatible
class NewsUsers(TimeMixin):
    email = models.EmailField(unique=True, max_length=30, blank=False, null=False, error_messages={'unique': 'This email has already been registered'})
    class Meta:
        verbose_name = _("NewsUser")
        verbose_name_plural = _("NewsUsers")

        def __str__(self):
            return self.email


@python_2_unicode_compatible
class Category(TimeMixin, MetaTagsMixin):
    """docstring for Category"""
    name = models.CharField(_("Category Name"), unique=True, max_length=255, blank=False, null=False)
    slug = models.SlugField(unique=True,null=True, blank=True, max_length=300)

    class Meta:
        verbose_name= _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.meta_keywords = self.name
        self.meta_author = "administrator 9bloggers"
        self.copyright = self.modified
        self.slug = slugify(self.name).lower()
        super().save(*args, **kwargs)



#the blogger has 1(single) object clap created for him which can be updated
#the clapper has many objects he can update through





@python_2_unicode_compatible
class Post(TimeMixin, MetaTagsMixin):
    """docstring for Post"""
    category = models.ForeignKey(Category,models.CASCADE, related_name="posts_in_category")
    topic    = models.CharField(_("Topic"), max_length=400, unique=True, error_messages={'unique': 'This topic has already been used', 'max_length':'The length should not exceed 500 characters'})
    #content  = models.TextField(_("Blog Content"),  max_length=12000, null=False, blank=False)
    content  = HTMLField(_('Blog Content'))
    slug     = models.SlugField(unique=True, max_length=500, null=True, blank=True)
    photos   = models.ImageField(storage=gpostc(), blank=False,null=False)
    post_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags     = models.TextField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name= _("Post")
        verbose_name_plural= _("Posts")
        get_latest_by = 'id'

    def __str__(self):
        return self.topic

    def tags_list(self):
        return self.tags.split(',')

    def save(self):
        self.meta_keywords = self.tags
        self.meta_description = '%s: %s' % (self.category.name, self.topic)
        self.meta_author = self.post_by.get_full_name()
        self.slug = slugify(self.topic).lower()
        self.meta_copyright = str(self.modified)


        try:
            super(Post, self).save()
        except Exception as e:
            print("\n\nErrors Occurred", e, "\n\n")




@python_2_unicode_compatible
class View(TimeMixin):
    num  = models.PositiveIntegerField(default=0)
    post = models.OneToOneField(Post, models.CASCADE, related_name="post_views")
    class Meta:
        verbose_name = _("View")
        verbose_name_plural = _("Views")

    def __str__(self):
        return str(self.num)


@python_2_unicode_compatible
class Clap(TimeMixin):
    num_claps = models.PositiveIntegerField(blank=True, default=0)
    post      = models.OneToOneField(Post, on_delete=models.CASCADE)
    clappers  = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'is_active': True}, related_name="post_clap_by")
    done      = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Clap"
        verbose_name_plural = "Claps"



    def __str__(self):
        return str(self.num_claps)




@python_2_unicode_compatible
class Like(TimeMixin):
    num_of_likes = models.PositiveIntegerField(blank=True, default=0)
    post     = models.OneToOneField(Post, related_name="likes_on_post", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'is_active': True}, related_name="post_liked_by")
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")


    def __str__(self):
        return str(self.num_of_likes)
