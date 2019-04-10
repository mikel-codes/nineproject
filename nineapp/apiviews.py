
#api/views.py

#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ClapSerializer, UserSerializer, LikeSerializer, PostSerializer, ViewSerializer
from .models import Clap, Like, Post, View


class ViewUpdate(generics.UpdateAPIView):
	serializer_class = ViewSerializer
	permission_classes = ()

	def update(self, request, pk):
		view = get_object_or_404(View, post=pk)
		view_data = ViewSerializer(view).data
		view_data['num'] += 1
		up_view = ViewSerializer(instance=view, data=view_data)
		if up_view.is_valid():
			up_view.save()
			return Response(up_view.data.get('num'), status=status.HTTP_200_OK)
		else:
			return Response(up_view.errors, status=status.HTTP_400_BAD_REQUEST)

class ClapUpdate(generics.UpdateAPIView):
	serializer_class = ClapSerializer
	permission_classes = (permissions.IsAuthenticated,)
	filter_fields = ('')

	def get_queryset(self):
		queryset = Post.objects.filter(post_by=self.kwargs['user_pk'])
		print("This is queryset ", queryset)
		total = 0
		for p in queryset:
			total += p.clap.num_claps
		return total

	def update(self, request, pk, user_pk, clapper_pk):
		clap = get_object_or_404(Clap, pk=pk)
		data = ClapSerializer(clap).data      # extract serialized data from saved clap object
		print(data)
		data['num_claps'] += request.data['num_claps']
		if int(request.data['clapper']) not in data['clappers']:
			print("\n not found\n")
			data['clappers'].append(request.data['clapper'])
			
			up_clap = ClapSerializer(instance=clap, data=data)
			if up_clap.is_valid():
				up_clap.save()
				total = self.get_queryset()
				print("\n\ntotal // ", total)
				return Response(total, status=status.HTTP_200_OK)
			else:
				return Response(up_clap.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			print("\nyes Found\n")
			return Response("you clapped here", status=status.HTTP_200_OK)


class UpdateLike(generics.UpdateAPIView):
	serializer_class = LikeSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def update(self, request, pk):
		like_obj = get_object_or_404(Like, pk=pk)
		data  = LikeSerializer(like_obj).data
		data['num_of_likes'] = request.data['num_of_likes']
		if int(request.data.get('liked_by')) not in data['liked_by']:
			print("\n not found\n")
			data['liked_by'].append(int(request.data.get('liked_by')))
		else:
			print("\nyes Found\n")
			return Response("you already liked this", status=status.HTTP_200_OK)

		up_like = LikeSerializer(instance=like_obj, data=data)
		if up_like.is_valid():
			up_like.save()
			return Response(up_like.data.get('num_of_likes'), status=status.HTTP_201_CREATED)
		else:
			return Response(up_like.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePostViews(generics.UpdateAPIView):
	serializer_class = PostSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request):
		pass