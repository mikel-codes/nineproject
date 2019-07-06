#-*- coding:utf-8 -*-
from  __future__ import unicode_literals
from django.urls import path, re_path
from .views import  (registration, dashboard, userlogin,
userlogout, reset, create_content, page_not_found, getpost, edit_post, delete_post, activate, edit_profile,
 contact, index, list_posts, activate, email_password_reset, password_reset_confirm, stripepay,no_js)

from django.conf.urls import url

from .apiviews import  ClapUpdate, UpdateLike, ViewUpdate
urlpatterns = [
	path("", index, name="indexpage"),
        path("member/new", registration, name="reg"),
        path("member/login", userlogin, name="signin"),
        path("user/<str:username>", dashboard, name="dashboard" ),
        path("logout", userlogout, name="logout"),
        path("password/reset", reset, name="reset_password"),
        path("page/new", create_content, name="new_content"),
        path("posts/edit/<int:pk>", edit_post, name="edit_post"),
        path("contact", contact, name="contact"),
        path("category/<str:slug>", list_posts, name="listposts"),

        # api views  -----------------------
        path("clap/<int:pk>/by/<int:clapper_pk>/for/<int:user_pk>", ClapUpdate.as_view(), name="clap_update"),
        #path('clap/<int:pk>', ClapDetail.as_view(), name="clap_detail"),
        path('like/change/<int:pk>', UpdateLike.as_view(), name="update_like"),
        path('update/view/<int:pk>', ViewUpdate.as_view(), name="view_update"),
        # ----------------------------------------------------------------

        path('member/login/email/password/reset', email_password_reset, name="email_reset"),

        path("disabled/javascript", no_js, name="no_js"),
        path('oops!',page_not_found, name="page_not_found" ),
        path('topic/<str:slug>', getpost, name ="getpost"),
        path('delete/<pk>', delete_post, name='deletepost'),
        path('<str:name>/profile', edit_profile, name="edit_profile"),
        # --------------- ------------------ -------------
        #Payments
        path('funding/', stripepay, name='payment'),
        # --------------- ------------------ -------------

        re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
        re_path(r'^reset/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',password_reset_confirm, name='password_reset_confirm'),

]