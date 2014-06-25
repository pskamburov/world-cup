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
import time
from datetime import datetime
import collections


def home(request):
    teams = Team.objects.all()
    return render(request, "home.html", locals())

def teams(request):
    teams = Team.objects.order_by('group')
    group_teams = collections.OrderedDict()
    for team in teams:
        group_teams.setdefault(team.group,[]).append(team)
    return render(request, "teams.html", locals())


def players(request):
    team_players = {}
    players = Player.objects.all()
    for player in players:
        team_players.setdefault(player.team, []).append(player)
    return render(request, "players.html", locals())

def ranking(request):
    user_points = []
    users = User.objects.all()
    for user in users:
        points_exists = Point.objects.filter(user=user)
        if points_exists:
            points = points_exists[0].points
        else:
            points = 0
        user_points.append((points,user.username))
        user_points.sort(reverse=True)
    return render(request, "ranking.html", locals())

def matches(request):
    matches = Match.objects.order_by('-schedule')
    return render(request, "matches.html", locals())


def show_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, "show-team.html", locals())

def show_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, "show-team.html", locals())

def show_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return render(request, "show-player.html", locals())


def show_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    MAX_VOTE = [str(x) for x in range(1, 6)]
    votes_players_host = {}
    votes_players_away = {}
    players_host = Player.objects.filter(team__name=match.host.name)
    votes_players_host = player_ratings(players_host, match_id)
    players_away = Player.objects.filter(team__name=match.away.name)
    votes_players_away = player_ratings(players_away, match_id)
    if request.user.is_authenticated():
        allowed = is_allowed(request.user)
        user_bet_exists = PredictMatch.objects.filter(predict_match=match,
                                               user=request.user)
        if user_bet_exists:
            user_bet = user_bet_exists[0]
        else:
            user_bet = None
    else:
        allowed = False
        user_bet = None


    all_bets = PredictMatch.objects.filter(predict_match=match)
    bets = {(bet.user, bet.score_host, bet.score_away, bet.goalscorer): 0
            for bet in all_bets}
    goals = Goal.objects.filter(match__id=match_id)
    goalscorers = [goal.goalscorer for goal in goals]
    for bet, points in bets.items():
        bets[bet] = calculate_points((bet[1], bet[2]),
                                     (match.score_host, match.score_away),
                                     bet[3], goalscorers)
    is_started = True if match_started(match) else False
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
        if bet_result == result:
            points = 5
        elif bet_difference == difference:
            points = 3
        elif (bet_difference > 0 and difference > 0) or\
                (bet_difference < 0 and difference < 0):
            points = 1
        for goalscorer in goalscorers:
            if goalscorer == bet_goalscorer:
                points += 1
    return points


def is_allowed(user):
    is_super = user.is_superuser
    allowed_group = set(['admin', 'moderator'])
    groups = [x.name for x in user.groups.all()]
    if allowed_group.intersection(set(groups)) or is_super:
        return True
    return False


def match_started(match):
    match_start = match.schedule.replace(tzinfo=None)
    now = datetime.now()
    if now > match_start:
        return True
    return False

def login(request):
    if request.user.is_authenticated():
        return redirect('my-profile')
    else:
        return views.login(request, template_name='login.html')


def my_profile(request):
    points_exists = Point.objects.filter(user=request.user)
    if points_exists:
        query_points = get_object_or_404(Point, user=request.user)
        points = query_points.points
    else:
        points = 0
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
                user = User.objects.create_user(username, email, password,
                                                first_name=first_name,
                                                last_name=last_name)
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        views.login(request, user)
                return redirect('login')
            else:
                match_flag = False
    return render(request, "register.html", locals())


@csrf_exempt
def betting(request):
    if request.user.is_authenticated():
        if request.is_ajax() and request.method == 'POST':
            user = request.user
            home_score = request.POST.get('home_score')
            away_score = request.POST.get('away_score')
            goalscorer_id = request.POST.get('goalscorer')
            match_id = request.POST.get('match_id')
            if not(home_score.isdigit() or away_score.isdigit()):
                message = "Incorrect type of scores!"
            elif goalscorer_id is None:
                message = "Please pick a goalscorer!"
            else:
                match = get_object_or_404(Match, id=match_id)
                if match_started(match):
                    message = "You can't bet. Match already started!"
                    return HttpResponse(message)
                player = get_object_or_404(Player, id=goalscorer_id)
                bet_query = PredictMatch(predict_match=match,
                                         goalscorer=player,
                                         score_host=home_score,
                                         score_away=away_score,
                                         user=user)
                bet_exists = PredictMatch.objects.filter(predict_match=match,
                                                         user=user)
                if bet_exists:
                    bet_exists.delete()
                bet_query.save()
                message = "Your bet was created successfully!".format(match.schedule.date)
        else:
            message = "No XHR"
        return HttpResponse(message)
    else:
        return HttpResponse("Please log-in to predict!")


@csrf_exempt
def addresult(request):
    if request.user.is_authenticated() and\
            is_allowed(request.user):
        if request.is_ajax() and request.method == 'POST':
            home_score = request.POST.get('home_score')
            away_score = request.POST.get('away_score')
            match_id = request.POST.get('match_id')
            if not(home_score.isdigit() or away_score.isdigit()):
                message = "Incorrect type of scores!"
            else:
                match = get_object_or_404(Match, id=match_id)
                if match.is_over:
                    message = "Match is over! Points have been given!"
                    return HttpResponse(message)
                match.score_host = home_score
                match.score_away = away_score
                match.save()
                message = "Result was updated successfully!{}"
        else:
            message = "No XHR"
        return HttpResponse(message)
    else:
        return HttpResponse("No permission!")


@csrf_exempt
def addgoal(request):
    if request.user.is_authenticated() and\
            is_allowed(request.user):
        if request.is_ajax() and request.method == 'POST':
            goalscorer_id = request.POST.get('goalscorer')
            match_id = request.POST.get('match_id')
            if not(match_id.isdigit() or goalscorer_id.isdigit()):
                message = "Incorrect data!"
            else:
                match = get_object_or_404(Match, id=match_id)
                player = get_object_or_404(Player, id=goalscorer_id)
                if match.is_over:
                    message = "Match is over! Points have been given!"
                else:
                    goal_query = Goal(match=match, goalscorer=player)
                    goal_query.save()
                    message = "Goalscorer was added successfully!{}"
        else:
            message = "No XHR"
        return HttpResponse(message)
    else:
        return HttpResponse("No permission!")


@csrf_exempt
def addpoints(request):
    if request.user.is_authenticated() and\
            is_allowed(request.user):
        if request.is_ajax() and request.method == 'POST':
            match_id = request.POST.get('match_id')
            if not match_id.isdigit():
                message = "Incorrect data!"
            else:
                match = get_object_or_404(Match, id=match_id)
                if match.is_over:
                    message = "Match is over! Points have been given!"
                    return HttpResponse(message)
                all_bets = PredictMatch.objects.filter(predict_match=match)
                goals = Goal.objects.filter(match=match)
                goalscorers = [goal.goalscorer for goal in goals]
                all_points = {}
                for bet in all_bets:
                    all_points[bet.user] = \
                        calculate_points((bet.score_host,
                                          bet.score_away),
                                         (match.score_host, match.score_away),
                                         bet.goalscorer, goalscorers)
                for user, points in all_points.items():
                    user_exists = Point.objects.filter(user=user)
                    if user_exists:
                        user_points = get_object_or_404(Point, user=user)
                        user_points.points += points
                    else:
                        user_points = Point(user=user, points=points)
                    user_points.save()
                match.is_over = True
                match.save()
                message = "Success {} ".format(user_points)

        else:
            message = "No XHR"
        return HttpResponse(message)
    else:
        return HttpResponse("No permission!")


@csrf_exempt
def rate(request):
    if request.user.is_authenticated():
        if request.is_ajax():
            if request.method == 'GET':
                message = "Failed"
            elif request.method == 'POST':
                user = request.user
                rating = request.POST.get('rating')
                player_id = request.POST.get('player_id')
                match_id = request.POST.get('match_id')
                match = get_object_or_404(Match, id=match_id)
                player = get_object_or_404(Player, id=player_id)
                if not Voting.objects.filter(match=match,
                                             player=player, user=user):
                    vote_query = Voting(match=match, player=player,
                                        vote=rating, user=user)
                    vote_query.save()
                    message = "You voted {} for {}. " \
                              "Thank you!".format(rating, player)
                else:
                    message = "You already voted for this player!"
        else:
            message = "No XHR"
        return HttpResponse(message)
    else:
        return HttpResponse("Please log-in to vote")