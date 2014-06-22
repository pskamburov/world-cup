# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=2)
    info = models.TextField()

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, related_name="team")
    age = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()
    position = models.CharField(max_length=3)

    def __str__(self):
        representation = "{}. {}".format(self.number, self.name)
        return representation


class Match(models.Model):
    host = models.ForeignKey(Team, related_name="host_matches")
    away = models.ForeignKey(Team, related_name="away_matches")
    score_host = models.PositiveSmallIntegerField(blank=True, null=True)
    score_away = models.PositiveSmallIntegerField(blank=True, null=True)
    schedule = models.DateTimeField()
    is_over = models.BooleanField(default=False)
    def __str__(self):
        representation = "{} {} : {} {}".format(self.host.name, self.score_host, self.score_away, self.away.name)
        return representation


class Goal(models.Model):
    match = models.ForeignKey(Match, related_name="match_g")
    goalscorer = models.ForeignKey(Player, related_name="scorer")


class Voting(models.Model):
    VOTE_CHOISES = (
            (1, "bad"),
            (2, "medium"),
            (3, "good"),
            (4, "very good"),
            (5, "excellent")
        )
    vote = models.PositiveSmallIntegerField(choices=VOTE_CHOISES,
       default=0)
    match = models.ForeignKey(Match, related_name="match")
    player = models.ForeignKey(Player, related_name="player")
    user = models.ForeignKey(User, related_name="user")


class Point(models.Model):
    user = models.ForeignKey(User, related_name="user_p")
    points = models.PositiveSmallIntegerField()


class PredictMatch(models.Model):
    predict_match = models.ForeignKey(Match, related_name="predict_match")
    user = models.ForeignKey(User, related_name="user_bet")
    score_host = models.PositiveSmallIntegerField()
    score_away = models.PositiveSmallIntegerField()
    goalscorer = models.ForeignKey(Player, related_name="goalscorer")
