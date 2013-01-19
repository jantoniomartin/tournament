import os.path

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from transmeta import TransMeta

class Tournament(models.Model):
	__metaclass__ = TransMeta
	
	slug = models.SlugField(_("slug"), max_length=20, unique=True)
	created_on = models.DateTimeField(_("created on"), auto_now_add=True)
	deadline = models.DateTimeField(_("registration deadline"))
	admission_open = models.BooleanField(_("admission is open"), default=False)
	auto_accept = models.BooleanField(_("automatically accept participants"), default=False)
	minimum_users = models.PositiveIntegerField(_("minimum users"), default=0)
	title = models.CharField(_("title"), max_length=100)
	description = models.TextField(_("description"))
	prize = models.TextField(_("prize"))
	rules = models.URLField(_("rules"))
	sponsors = models.ManyToManyField('Sponsor', null=True, blank=True)

	class Meta:
		verbose_name = _("tournament")
		verbose_name_plural = _("tournaments")
		ordering = ["created_on",]
		translate = ('title', 'description', 'prize', 'rules')

	def __unicode__(self):
		return self.slug

	def extend_deadline(self):
		"""
		When there are fewer participants than the minimum, extend the admission deadline
		"""
		self.deadline = self.deadline + datetime.timedelta(seconds=24*60*60)
		self.save()
		logger.info("Extended tournament deadline.")

def get_banner_upload_path(instance, filename):
	return os.path.join(settings.MEDIA_ROOT, "banners", instance.banner_filename)

class Sponsor(models.Model):
	name = models.CharField(_("name"), max_length=100)
	motto = models.CharField(_("motto"), max_length=200)
	banner = models.ImageField(_("banner"), upload_to=get_banner_upload_path)
	url = models.URLField()

	class Meta:
		verbose_name = _("sponsor")
		verbose_name_plural = _("sponsors")

	def __unicode__(self):
		return self.name

	def _get_banner_filename(self):
		return "%s.png" % slugify(self.name)

	banner_filename = property(_get_banner_filename)

class Participant(models.Model):
	user = models.ForeignKey(User)
	tournament = models.ForeignKey(Tournament)
	joined_on = models.DateTimeField(_("joined_on"), auto_now_add=True)
	accepted = models.BooleanField(_("accepted"), default=False)
	eliminated = models.BooleanField(_("eliminated"), default=False)

	class Meta:
		verbose_name = _("participant")
		verbose_name_plural = _("participants")
		unique_together = (("user", "tournament"),)

	def __unicode__(self):
		return unicode(self.user)

	def save(self, *args, **kwargs):
		if not self.pk:
			if self.tournament.auto_accept:
				self.accepted = True
		super(Participant, self).save(*args, **kwargs)
