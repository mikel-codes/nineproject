from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Post, Category, Clap, Profile, Like
# Register your models here.

admin.site.register(Category)

admin.site.register(Clap)
admin.site.register(Post)
admin.site.register(Like)

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	fk_name = 'author'
	verbose_name_plural = 'Profile'

class CustomAdminUser(UserAdmin):
	inlines = (ProfileInline, )
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_location')
	list_select_related = ('profile', )
	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super().get_inline_instances(request, obj)

	def get_location(self, instance):
		return instance.profile.location
	get_location.short_description = 'Location'


admin.site.unregister(User)
admin.site.register(User, CustomAdminUser)
admin.site.register(Profile)