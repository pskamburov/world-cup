from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Player, Match, Voting, Point, PredictMatch, Goal

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
    votes_players_host = player_ratings(players_host, match_id)
    players_away = Player.objects.filter(team__name=match.away.name)
    votes_players_away = player_ratings(players_away, match_id)

    if request.user.is_authenticated():
        username = request.user.username
        is_super = request.user.is_superuser
        allowed = is_allowed(username) or is_super

    else:
        allowed = False
    all_bets = PredictMatch.objects.filter(predict_match__id=match_id)
    bets = { (bet.user, bet.score_host, bet.score_away, bet.goalscorer):0 for bet in all_bets}
    goals = Goal.objects.filter(match__id=match_id)
    goalscorers = [ goal.goalscorer for goal in goals ]
    for bet, points in bets.items():
        bets[bet] = calculate_points((bet[1], bet[2]),(match.score_host, match.score_away), bet[3], goalscorers)
    is_over = match.is_over
    if is_over:
        pass
    return render(request, "show-match.html", locals())

def player_ratings(players, match_id):
    player_votes = {}
    for player in players:
        all_votes = Voting.objects.filter(match__id=match_id, player=player)
        sum_vote = sum([query.vote for query in all_votes])
        count = 1 if all_votes.count() == 0 else all_votes.count()
        player_votes[player] = sum_vote/count
    return player_votes

def calculate_points(bet_result, result, bet_goalscorer, goalscorers):
    points = 0
    if result != (None, None):
        bet_difference = bet_result[0] - bet_result[1]
        difference = result[0] - result[1]
        if( bet_result == result):
            points = 5
        elif (bet_difference == difference ):
            points = 3
        elif ((bet_difference > 0 and difference > 0) or (bet_difference < 0 and difference < 0)):
            points = 1
        for goalscorer in goalscorers:
            if(goalscorer == bet_goalscorer):
                points += 1
    return points

def is_allowed(user):
    allowed_group = set(['admin', 'moderator'])
    usr = User.objects.get(username=user)
    groups = [ x.name for x in usr.groups.all()]
    if allowed_group.intersection(set(groups)):
       return True
    return False

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