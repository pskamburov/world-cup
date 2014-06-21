from django.contrib import admin
from .models import Team, Player, Match, Voting, Point, PredictMatch, Goal

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

class PointAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')

class GoalAdmin(admin.ModelAdmin):
    list_display = ('match', 'goalscorer')

class VotingAdmin(admin.ModelAdmin):
    list_display = ('player', 'vote', 'user', 'match')

admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Point, PointAdmin)
admin.site.register(Match)
admin.site.register(PredictMatch)
admin.site.register(Voting, VotingAdmin)