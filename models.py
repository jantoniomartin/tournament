import os.path

import logging
logger = logging.getLogger(__name__)
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from transmeta import TransMeta

import condottieri_scenarios.models as scenarios
import machiavelli.models as machiavelli

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
	created_by = models.ForeignKey(User)

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

class Stage(models.Model):
	tournament = models.ForeignKey(Tournament)
	number = models.PositiveIntegerField(_("number"), default=0)
	size = models.PositiveIntegerField(_("size"), default=0)
	number_of_games = models.PositiveIntegerField(_("number of games"), default=0)
	started_on = models.DateTimeField(_("started on"), null=True, blank=True)
	finished_on = models.DateTimeField(_("finished on"), null=True, blank=True)	
	scenario = models.ForeignKey(scenarios.Scenario)
	time_limit = models.PositiveIntegerField(_("time limit"), default=24*60*60,
		help_text = _("seconds available to play a turn"))
	cities_to_win = models.PositiveIntegerField(_("cities to win"), default=15,
		help_text=_("cities that must be controlled to win a game"))
	years_limit = models.PositiveIntegerField(_("years limit"), default=0,
		help_text=_("the game finish after these years"))
	users = models.ManyToManyField(User, through="Slot") 
	
	class Meta:
		verbose_name = _("stage")
		verbose_name_plural = _("stages")
		unique_together = (("tournament", "number"),)

	def __unicode__(self):
		return _("Stage %s in %s") % (self.number, self.tournament.title)

	def create_slots(self):
		""" Creates a new slot in this stage for all the tournament participants that has not
		been eliminated."""
		participants = self.tournament.participant_set.filter(accepted=True, eliminated=False)
		for p in participants:
			slot = Slot(user=p.user, stage=self)
			slot.save()
			logger.info("Added slot for %s" % p.user)

	def create_empty_games(self):
		for i in range (0, self.number_of_games):
			title = "%s-%s-%s" % (self.tournament.slug, self.number, i)
			g = TournamentGame(title=title, stage=self)
			g.save()

	#def create_games(self):
	#	player_list_size = self.number_of_games * self.scenario.number_of_players
	#	base_list = list(self.users.all())

		
	
class Configuration(models.Model):
	""" Defines the common configuration options for each game in a stage. 
	"""

	stage = models.OneToOneField(Stage, verbose_name=_('stage'), editable=False)
	finances = models.BooleanField(_('finances'), default=False)
	assassinations = models.BooleanField(_('assassinations'), default=False,
					help_text=_('will enable Finances'))
	excommunication = models.BooleanField(_('excommunication'), default=False)
	special_units = models.BooleanField(_('special units'), default=False,
					help_text=_('will enable Finances'))
	lenders = models.BooleanField(_('money lenders'), default=False,
					help_text=_('will enable Finances'))
	unbalanced_loans = models.BooleanField(_('unbalanced loans'), default=False,
		help_text=_('the credit for all players will be 25d'))
	conquering = models.BooleanField(_('conquering'), default=False)
	famine = models.BooleanField(_('famine'), default=False)
	plague = models.BooleanField(_('plague'), default=False)
	storms = models.BooleanField(_('storms'), default=False)
	strategic = models.BooleanField(_('strategic movement'), default=False)
	variable_home = models.BooleanField(_('variable home country'), default=False, help_text=_('conquering will be disabled'))
	taxation = models.BooleanField(_('taxation'), default=False,
					help_text=_('will enable Finances and Famine'))
	fow = models.BooleanField(_('fog of war'), default=False,
		help_text=_('each player sees only what happens near his borders'))
	press = models.PositiveIntegerField(_('press'), choices=machiavelli.PRESS_TYPES, default=0)

	def __unicode__(self):
		return _("Configuration for %s") % self.stage

	def get_enabled_rules(self):
		rules = []
		for f in self._meta.fields:
			if isinstance(f, models.BooleanField):
				if f.value_from_object(self):
					rules.append(unicode(f.verbose_name))
		return rules

	def _get_gossip(self):
		if self.press in (0, 2):
			return True
		return False

	gossip = property(_get_gossip)

	def _get_letters(self):
		return self.press == 0

	letters = property(_get_letters)

	def _get_public_gossip(self):
		return self.press == 2

	public_gossip = property(_get_public_gossip)
	
#def create_configuration(sender, instance, created, **kwargs):
#    if isinstance(instance, Stage) and created:
#		config = Configuration(stage=instance)
#		config.save()
#
#models.signals.post_save.connect(create_configuration, sender=Stage)

class Slot(models.Model):
	""" A Slot defines the participation of a User in a Stage.
	"""
	user = models.ForeignKey(User)
	stage = models.ForeignKey(Stage)
	score = models.PositiveIntegerField(_("score"), blank=True, null=True)

	class Meta:
		verbose_name = _("slot")
		verbose_name_plural = _("slots")
		unique_together = (("user", "stage"),)

	def __unicode__(self):
		return unicode(self.user)

class TournamentGame(machiavelli.Game):
	stage = models.ForeignKey(Stage)

	class Meta:
		verbose_name = _("tournament game")
		verbose_name_plural = _("tournament games")
	
	def save(self, *args, **kwargs):
		""" Fill some properties common to tournament games """
		if not self.pk:
			s = self.stage
			self.slots = 0
			self.scenario = s.scenario
			self.created_by = s.tournament.created_by
			self.visible = False
			self.time_limit = s.time_limit
			self.autostart = True
			self.cities_to_win = s.cities_to_win
			self.years_limit = s.years_limit
			self.fast = False
			self.uses_karma = False
			self.private = False
		super(TournamentGame, self).save(*args, **kwargs)

def configure_game(sender, instance, created=False, **kwargs):
	"""
	Creates a Configuration object for the new game
	"""
	if created:
		config = machiavelli.Configuration(game=instance)
		config.finances = s.configuration.finances
		config.assassination = s.configuration.assassinations
		config.excommunication = s.configuration.excommunication
		config.special_units = s.configuration.special_units
		config.lenders = s.configuration.lenders
		config.unbalanced_loans = s.configuration.unbalanced_loans
		config.conquering = s.configuration.conquering
		config.famine = s.configuration.famine
		config.plague = s.configuration.plague
		config.storms = s.configuration.storms
		config.strategic = s.configuration.strategic
		config.press = s.configuration.press
		config.save()

models.signals.post_save.connect(configure_game, sender=TournamentGame)
