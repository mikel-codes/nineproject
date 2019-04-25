from rest_framework import serializers
from .models import Clap, User, Like, Post, View

class ClapSerializer(serializers.ModelSerializer):
	class Meta:
		model  = Clap
		fields = ('num_claps','post','clappers')

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Like
		fields = ('num_of_likes', 'post', 'liked_by')

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ("views",)

class ViewSerializer(serializers.ModelSerializer):
	class Meta:
		model = View
		fields = ("num", "post",)