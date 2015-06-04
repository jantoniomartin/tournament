from django.conf.urls import *

import tournament.views as views

urlpatterns = patterns('tournament.views',
	url(r'^$', views.LatestTournamentDetailView.as_view(), name="latest-tournament"), 
	url(r'^(?P<slug>\w+)$', views.TournamentDetailView.as_view(), name="tournament-detail"),
	url(r'^register/(?P<slug>\w+)$', views.RegisterParticipantView.as_view(), name="register-participant"),
	url(r'^active/(?P<slug>\w+)$', views.ActiveGamesListView.as_view(), name="tournament-active-games"),
	url(r'^finished/(?P<slug>\w+)$', views.FinishedGamesListView.as_view(), name="tournament-finished-games"),
)
