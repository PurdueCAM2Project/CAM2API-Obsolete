from django.conf import settings 
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import binascii
import os


@python_2_unicode_compatible
class Token(models.Model):
	key = models.CharField(_("Key"), max_length=40, primary_key=True)
	created = models.DateTimeField(_("Created"), auto_now_add=True)
	access_times = models.PositiveIntegerField(_("Access_times"), default=0)
	permission = models.CharField(_("Permission"), max_length=20, default="BaseUser")

	class Meta:
		abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
		verbose_name = _("Token")
		verbose_name_plural = _("Tokens")

	def save(self, *args, **kwargs):
		if not self.key:
			self.key = self.generate_key()
		return super(Token, self).save(*args, **kwargs)

	def generate_key(self):
		return binascii.hexlify(os.urandom(20)).decode()

	def __str__(self):
		return self.key

