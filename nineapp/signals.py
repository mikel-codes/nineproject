#signals.py

# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User

from .models import Clap, Post, Like, Profile, View

@receiver(post_save, sender=User, dispatch_uid="create_profile")
def create_user_profile(sender, instance, created, **kwargs):
	if instance.is_active is True:
		Profile.objects.get_or_create(author=instance)
		instance.profile.save()


@receiver(post_save, sender=Post, dispatch_uid="like")
def create_like_for_new_post(sender, instance, created, **kwargs):
	Like.objects.get_or_create(post=instance)
	print("\nCreated 0 like for new post\n")

@receiver(post_save, sender=User, dispatch_uid="create_token")
def create_api_token_for_new_user(sender, instance, created, update_fields=('is_active',),**kwargs):
	if instance.is_active is True:
		Token.objects.get_or_create(user=instance)
		print("\n\ntoken was successfully created for user", instance.username, "\n\n")

@receiver(post_save, sender=Post, dispatch_uid="create_clap")
def create_clap_for_new_user_post(sender, instance, created, **kwargs):
	Clap.objects.get_or_create(post=instance)
	print("\n\nCreated 1 clap for new user\n\n")


@receiver(post_save, sender=Post, dispatch_uid="create_a_view")
def create_new_view(sender, instance, created, **kwargs):
	View.objects.get_or_create(post=instance)
	print("View set for post", instance.topic)
	
	