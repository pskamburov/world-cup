from django.contrib import admin
from .models import Team, Player, Match, Voting

class TeamAdmin(admin.ModelAdmin):
    # fields = ['name', 'group', 'info']
    fieldsets = [
    (None,               {'fields': ['name']}),
    ('Description: : ', {'fields': ['group', 'info']}),
    # ('Info: ', {'fields': ['info']}),
]
    list_display = ('name', 'group')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')


class VotingAdmin(admin.ModelAdmin):
    list_display = ('player', 'vote', 'user', 'match')

admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match)
admin.site.register(Voting, VotingAdmin)