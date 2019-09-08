from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator

import tournament.models as tournament

class TournamentDetailView(DetailView):
	context_object_name = "tournament"
	model = tournament.Tournament

class LatestTournamentDetailView(TournamentDetailView):
	#queryset = tournament.Tournament.objects.latest('created_on')

	def get_object(self):
		return tournament.Tournament.objects.latest('created_on')
	
	def get_context_data(self, **kwargs):
		context = super(LatestTournamentDetailView, self).get_context_data(**kwargs)
		t = self.get_object()
		try:
			current_stage = tournament.Stage.objects.get(tournament=t, started_on__isnull=False,
				finished_on__isnull=True)
		except ObjectDoesNotExist as MultipleObjectsReturned:
			current_stage = tournament.Stage.objects.none()
		context.update({"current_stage": current_stage,})
		
		return context

class RegisterParticipantView(TemplateView):
	template_name = "tournament/register.html"

	def get(self, request, **kwargs):
		context = {}
		t = get_object_or_404(tournament.Tournament, slug=kwargs['slug'])
		context.update({'tournament': t})
		try:
			tournament.Participant.objects.get(tournament=t, user=request.user)
		except ObjectDoesNotExist:
			p = tournament.Participant(user=request.user, tournament=t)
			p.save()
			context.update({'message': _("You have been registered successfully.")})
		else:
			context.update({'message': _("You are already registered in this tournament.")})
			
		return self.render_to_response(context)

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(RegisterParticipantView, self).dispatch(*args, **kwargs)

class ActiveGamesListView(ListView):
	template_name = 'tournament/game_list_active.html'
	model = tournament.TournamentGame
	paginate_by = 10
	context_object_name = 'game_list'
	
	def get_queryset(self):
		t = get_object_or_404(tournament.Tournament, slug=self.kwargs['slug'])
		return tournament.TournamentGame.objects.filter(stage__tournament=t,
			started__isnull=False, finished__isnull=True)
	
	def get_context_data(self, **kwargs):
		context = super(ActiveGamesListView, self).get_context_data(**kwargs)
		t = get_object_or_404(tournament.Tournament, slug=self.kwargs['slug'])
		context.update({"tournament": t})
		return context

class FinishedGamesListView(ListView):
	template_name = 'tournament/game_list_finished.html'
	model = tournament.TournamentGame
	paginate_by = 10
	context_object_name = 'game_list'
	
	def get_queryset(self):
		t = get_object_or_404(tournament.Tournament, slug=self.kwargs['slug'])
		return tournament.TournamentGame.objects.filter(stage__tournament=t,
			started__isnull=False, finished__isnull=False)
	
	def get_context_data(self, **kwargs):
		context = super(FinishedGamesListView, self).get_context_data(**kwargs)
		t = get_object_or_404(tournament.Tournament, slug=self.kwargs['slug'])
		context.update({"tournament": t})
		return context


