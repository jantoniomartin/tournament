from django.contrib import admin

import tournament.models as tournament

admin.site.register(tournament.Participant)
admin.site.register(tournament.Sponsor)
admin.site.register(tournament.Tournament)
