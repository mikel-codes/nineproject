# -*- utf:8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import escape
from django.utils.safestring import mark_safe


class TimeMixin(models.Model):
	created  = models.DateTimeField(_("Created on"), editable=False, auto_now_add=True)
	modified = models.DateTimeField(_("Modified on"), editable=False, auto_now=True)

	class Meta:
		abstract = True


class MetaTagsMixin(models.Model):
	meta_keywords = models.CharField(
		_("Keywords"),max_length=255,
		blank=True,
		help_text=_("Separate keywords by comma."),
		)

	meta_description = models.CharField(
		_("Description"),max_length=255,
		blank=True,
		)

	meta_author = models.CharField(
		_("Author"),
		max_length=255,
		blank=True,
		)

	meta_copyright = models.CharField(
		_("Copyright"),max_length=255,blank=True,
		)

	class Meta:
		abstract = True

	def get_meta_keywords(self):
		tag = ""
		if self.meta_keywords:
			tag = '<meta name="keywords" content="%s" />\n' % escape(self.meta_keywords)
		return mark_safe(tag)

	def get_meta_description(self):
		tag = ""
		if self.meta_description:
			tag = '<meta name="description" content="%s" />\n' % escape(self.meta_description)
		return mark_safe(tag)

	def get_meta_author(self):
		tag  = ""
		if self.meta_author:
			tag = '<meta name="author" content="%s" />\n' % escape(self.meta_author)
		return tag

	def get_meta_copyright(self):
		tag = ""
		if self.meta_copyright:
			tag = '<meta name="copyright" content="%s" />\n' % escape(self.meta_copyright)
		return mark_safe(tag)

	def get_meta_tags(self):
		return mark_safe("".join((
			self.get_meta_keywords(),
			self.get_meta_description(),
			self.get_meta_author(),
			self.get_meta_copyright()
		)))

    