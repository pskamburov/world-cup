from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Player, Match, Voting

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    teams = Team.objects.all()
    return render(request, "home.html", locals())

def teams(request):
    teams = Team.objects.all()
    return render(request, "teams.html", locals())

def players(request):
    players = Player.objects.all()
    return render(request, "players.html", locals())

def matches(request):
    matches = Match.objects.all()
    return render(request, "matches.html", locals())

def show_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, "show-team.html", locals())

def show_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return render(request, "show-player.html", locals())

def show_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    MAX_VOTE = [str(x) for x in range(1,6)]
    votes_players_host = {}
    votes_players_away = {}
    players_host = Player.objects.filter(team__name=match.host.name)
    for player in players_host:
        all_votes = Voting.objects.filter(match__id=match_id, player=player)
        sum_vote = sum([query.vote for query in all_votes])
        count = 1 if all_votes.count() == 0 else all_votes.count()
        votes_players_host[player] = sum_vote/count
    players_away = Player.objects.filter(team__name=match.away.name)
    for player in players_away:
        all_votes = Voting.objects.filter(match__id=match_id, player=player)
        sum_vote = sum([query.vote for query in all_votes])
        count = 1 if all_votes.count() == 0 else all_votes.count()
        votes_players_away[player] = sum_vote/count
    return render(request, "show-match.html", locals())


def login(request):
    if request.user.is_authenticated():
        return redirect('my-profile')
    else:
        return views.login(request, template_name='login.html')

def my_profile(request):
    return render(request, "my_profile.html", locals())

def logout(request):
    views.logout(request)
    return redirect('login')

def register(request):
    data = request.POST if request.POST else None
    form = RegistrationForm(data)
    match_flag = True
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            if password == repeat_password:
                user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        views.login(request, user)
                return redirect('login')
            else:
                match_flag = False
    return render(request, "register.html", locals())


@csrf_exempt
def rate(request):
    if request.user.is_authenticated():
        if request.is_ajax():
            if request.method == 'GET':
                message = "Failed"
            elif request.method == 'POST':
                username = request.POST.get('user')
                rating = request.POST.get('rating')
                player_id = request.POST.get('player_id')
                match_id = request.POST.get('match_id')
                match = get_object_or_404(Match, id=match_id)
                player = get_object_or_404(Player, id=player_id)
                user = get_object_or_404(User, username=username)
                if not Voting.objects.filter(match=match, player=player, user=user):
                    vote_query = Voting(match=match, player=player, vote=rating, user=user)
                    vote_query.save()
                    message = "You voted {} for {}. Thank you!".format(rating, player)
                else:
                    message = "You already voted for this player!"

        else:
            message = "No XHR"
        return HttpResponse(message)
    else:
        return HttpResponse("Please log-in to vote")