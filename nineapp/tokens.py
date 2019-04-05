#tokens.oy for generating unique hash for user account activation

#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.utils import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator as PRTG

class AccountTokenGenerator(PRTG):
	
	def __init__(self, *args,**kwargs):
		super(AccountTokenGenerator, self).__init__(*args, **kwargs)

	def __make_hash_value(self, user, timestamp):
		return (six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active))


account_token = AccountTokenGenerator()
