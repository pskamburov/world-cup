from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from .models import Match, Team, Player, Point, Voting, PredictMatch, Goal
from .views import player_ratings, calculate_points, match_started
import time
import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404


class WebsiteViewsTestCase(TestCase):

    def setUp(self):
        self.username = 'petar'
        self.email = 'petar@abv.bg'
        self.password = '321'
        self.test_user = User.objects.create_user(
            self.username,
            self.email,
            self.password)
        self.team = Team(name="England", group="A", info="england team info")
        self.team.save()
        self.second_team = Team(name="Brazil", group="B", info="brazil info")
        self.second_team.save()
        self.player = Player(name="Lampard", team=self.team,
                             age=34, number=8, position="MF")
        self.second_player = Player(name="Rooney", team=self.team,
                                    age=28, number=10, position="FW")
        self.third_player = Player(name="Neymar", team=self.second_team,
                                   age=23, number=10, position="FW")
        self.player.save()
        self.second_player.save()
        self.third_player.save()
        self.match = Match(host=self.team,
                           away=self.second_team,
                           score_host=2,
                           score_away=2,
                           schedule=datetime.date.today() +
                           datetime.timedelta(days=3),
                           is_over=False)
        self.match.save()
        self.vote1 = Voting(vote=5, match=self.match,
                            player=self.player, user=self.test_user)
        self.vote2 = Voting(vote=5, match=self.match,
                            player=self.second_player, user=self.test_user)
        self.vote3 = Voting(vote=5, match=self.match,
                            player=self.third_player, user=self.test_user)
        self.vote1.save()
        self.vote2.save()
        self.vote3.save()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_my_profile(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)

    def test_players(self):
        response = self.client.get('/players')
        self.assertTrue(self.player in
                        response.context["team_players"][self.team])
        self.assertEqual(response.status_code, 200)

    def test_players_order_by_teams(self):
        response = self.client.get('/players')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["team_players"][self.team],
                         [self.player, self.second_player])
        self.assertEqual(response.context["team_players"][self.second_team],
                         [self.third_player])

    def test_teams(self):
        team = Team(name="Brazil", group="A", info="brazil team info")
        team.save()
        response = self.client.get('/teams')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(team in response.context["teams"])
        self.assertEqual(response.status_code, 200)

    def test_teams_order_by_groups(self):
        response = self.client.get('/teams')
        self.assertEqual(response.context["group_teams"]["A"], [self.team])
        self.assertEqual(response.context["group_teams"]["B"],
                         [self.second_team])

    def test_matches(self):
        response = self.client.get('/matches')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.match in response.context["matches"])

    def test_show_team(self):
        response = self.client.get('/team/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["team"], self.team)

    def test_show_player(self):
        response = self.client.get('/player/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["player"], self.player)

    def test_show_match(self):
        resp = self.client.get('/match/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["match"], self.match)
        self.assertEqual(resp.context["is_started"], False)

    def test_rankings(self):
        response = self.client.get('/ranking/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user_points"],
                         [(0, self.username)])
        user_point = Point(user=self.test_user, points=5)
        user_point.save()
        second_response = self.client.get('/ranking/')
        self.assertEqual(second_response.context["user_points"],
                         [(5, self.username)])

    def test_player_ratings(self):
        ratings = player_ratings(
            [self.player, self.second_player, self.third_player],
            self.match.id)
        self.assertEqual(ratings[self.player], 5)

    def test_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        login = self.client.login(
            username=self.username,
            password=self.password)
        self.assertEqual(login, True)

    def test_calculate_points(self):
        points = calculate_points((0, 1), (0, 2),
                                  self.player,
                                  [self.second_player])
        score_points = calculate_points((0, 2), (0, 2),
                                        self.player,
                                        [self.second_player])
        differ_points = calculate_points((0, 2), (2, 4),
                                         self.player,
                                         [self.player,
                                          self.player])
        self.assertEqual(points, 1)
        self.assertEqual(score_points, 5)
        self.assertEqual(differ_points, 5)

    def test_betting(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        resp_post = self.client.post('/betting/', {
            'home_score': "4",
            'away_score': "1",
            'goalscorer': "1",
            'match_id': "1"}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp_post.status_code, 200)
        self.assertEqual(resp_post.content,
                         b'Your bet was created successfully!')
        self.assertEqual(len(PredictMatch.objects.all()), 1)

    def test_rating_fail(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        resp_post = self.client.post('/rate/', {
            'rating': "5",
            'player_id': "1",
            'match_id': "1"}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp_post.status_code, 200)
        self.assertEqual(resp_post.content,
                         b'You already voted for this player!')
        self.assertEqual(len(Voting.objects.all()), 3)

    def test_rating_success(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        test_player = Player(name="Iniesta", team=self.second_team,
                             age=23, number=8, position="FW")
        test_player.save()
        resp_post = self.client.post('/rate/', {
            'rating': "5",
            'player_id': "4",
            'match_id': "1"}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp_post.status_code, 200)
        self.assertEqual(resp_post.content,
                         b'You voted 5 for 8. Iniesta. Thank you!')
        self.assertEqual(len(Voting.objects.all()), 4)

    def test_addresult(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        resp_post = self.client.post('/addresult/', {
            'home_score': "4",
            'away_score': "1",
            'match_id': "1"}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp_post.status_code, 200)
        self.assertEqual(resp_post.content, b'No permission!')
        added_match = get_object_or_404(Match, id=1)
        self.assertEqual(added_match, self.match)

    def test_addgoal(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        resp_post = self.client.post('/addgoal/', {
            'goalscorer': "4",
            'match_id': "1"}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp_post.status_code, 200)
        self.assertEqual(resp_post.content, b'No permission!')
        self.assertEqual(len(Goal.objects.all()), 0)

    def test_addpoints(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        resp_post = self.client.post('/addpoints/', {
            'match_id': "1"}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp_post.status_code, 200)
        self.assertEqual(resp_post.content, b'No permission!')
        self.assertEqual(len(Point.objects.all()), 0)