from django.apps import AppConfig


class NineappConfig(AppConfig):
    name = 'nineapp'

    def ready(self):
    	from nineapp.signals import create_api_token_for_new_user,  create_like_for_new_post, create_clap_for_new_user_post, create_user_profile, create_new_view

