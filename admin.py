from django.contrib import admin

import tournament.models as tournament

class ConfigurationInline(admin.TabularInline):
	model = tournament.Configuration
	extra = 1


class SlotInline(admin.TabularInline):
	model = tournament.Slot
	extra = 5

class StageAdmin(admin.ModelAdmin):
	inlines = [ConfigurationInline, SlotInline,]

admin.site.register(tournament.Participant)
admin.site.register(tournament.Sponsor)
admin.site.register(tournament.Stage, StageAdmin)
admin.site.register(tournament.Tournament)
admin.site.register(tournament.TournamentGame)
