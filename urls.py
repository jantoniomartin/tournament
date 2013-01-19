from django.conf.urls.defaults import *

import tournament.views as views

urlpatterns = patterns('tournament.views',
	url(r'^$', views.LatestTournamentDetailView.as_view(), name="latest-tournament"), 
	url(r'^(?P<slug>\w+)$', views.TournamentDetailView.as_view(), name="tournament-detail"),
	url(r'^register/(?P<slug>\w+)$', views.RegisterParticipantView.as_view(), name="register-participant"),
)
