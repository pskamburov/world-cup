from django.conf.urls import patterns, include, url

urlpatterns = patterns('website.views',
    url(r'^$', 'home', name="home"),
    url(r'^matches$', 'matches', name="matches"),
    url(r'^teams$', 'teams', name="teams"),
    url(r'^players$', 'players', name="players"),
    url(r'^match/(?P<match_id>[0-9]+)/$', 'show_match', name="show-match"),
    url(r'^team/(?P<team_id>[0-9]+)/$', 'show_team', name='show-team'),
    url(r'^player/(?P<player_id>[0-9]+)/$', 'show_player', name='show-player'),
    url(r'login$', 'login', name='login'),
    url(r'^accounts/profile/$', 'my_profile', name='my-profile'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^register/$', 'register', name='register'),
    url(r'^rate/$', 'rate', name='rate'),
    url(r'^betting/$', 'betting', name='betting'),
    url(r'^addresult/$', 'addresult', name='addresult'),
    url(r'^addgoal/$', 'addgoal', name='addgoal'),
    url(r'^addpoints/$', 'addpoints', name='addpoints'),

)