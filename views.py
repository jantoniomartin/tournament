from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator

import tournament.models as tournament

class TournamentDetailView(DetailView):
	context_object_name = "tournament"
	model = tournament.Tournament

class LatestTournamentDetailView(TournamentDetailView):
	#queryset = tournament.Tournament.objects.latest('created_on')

	def get_object(self):
		return tournament.Tournament.objects.latest('created_on')

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
