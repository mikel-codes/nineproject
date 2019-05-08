#tokens.oy for generating unique hash for user account activation

#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.utils import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator as PRTG

class AccountTokenGenerator(PRTG):
	def _make_hash_value(self, user, timestamp):
		return (six.text_type(user) + six.text_type(timestamp) + six.text_type(user.is_active))


account_token = AccountTokenGenerator()
