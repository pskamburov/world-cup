# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    """A specified team

    Attributes:
    name -- Name of the team
    group -- Group of the team
    info -- Information for the team
    """
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=2)
    info = models.TextField()

    def __str__(self):
        return self.name


class Player(models.Model):
    """A specified player

    Attributes:
    name -- Name of the player
    team -- The team of the player
    age -- Age of the player
    number -- Number of the player
    position -- Position of the player(MF/FW/GK/DF)
    """
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, related_name="team")
    age = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()
    position = models.CharField(max_length=3)

    def __str__(self):
        representation = "{}. {}".format(self.number, self.name)
        return representation


class Match(models.Model):
    """A specified match

    Attributes:
    host -- Name of the host team
    away -- Name of the away team
    score_host -- Host score
    score_away -- Away score
    schedule -- The date and time when match starts
    is_over -- Bool field to check if match is over
    """
    host = models.ForeignKey(Team, related_name="host_matches")
    away = models.ForeignKey(Team, related_name="away_matches")
    score_host = models.PositiveSmallIntegerField(blank=True, null=True)
    score_away = models.PositiveSmallIntegerField(blank=True, null=True)
    schedule = models.DateTimeField()
    is_over = models.BooleanField(default=False)

    def __str__(self):
        if self.score_host is None or self.score_away is None:
            score_host = ""
            score_away = ""
        else:
            score_host = self.score_host
            score_away = self.score_away
        representation = "{} {} : {} {}".format(self.host.name,
                                                score_host,
                                                score_away,
                                                self.away.name)
        return representation


class Goal(models.Model):
    """A specified goal

    Attributes:
    match -- Match when the goal is scored
    goalscorer -- Player who scored the goal
    """
    match = models.ForeignKey(Match, related_name="match_g")
    goalscorer = models.ForeignKey(Player, related_name="scorer")


class Voting(models.Model):
    """A specified vote to a player

    Attributes:
    vote -- The user vote (1-5)
    match -- The match
    player -- The rated player
    user -- User who vote
    """
    VOTE_CHOISES = (
        (1, "bad"),
        (2, "medium"),
        (3, "good"),
        (4, "very good"),
        (5, "excellent"))
    vote = models.PositiveSmallIntegerField(choices=VOTE_CHOISES,
                                            default=0)
    match = models.ForeignKey(Match, related_name="match")
    player = models.ForeignKey(Player, related_name="player")
    user = models.ForeignKey(User, related_name="user")


class Point(models.Model):
    """Points for users

    Attributes:
    user -- User
    points -- All points of user
    """
    user = models.ForeignKey(User, related_name="user_p")
    points = models.PositiveSmallIntegerField()


class PredictMatch(models.Model):
    """Predicted match

    Attributes:
    predict_match -- Predicted match
    user -- User
    score_host -- Host score
    score_away -- Away score
    goalscorer -- Predicted goalscorer
    """
    predict_match = models.ForeignKey(Match, related_name="predict_match")
    user = models.ForeignKey(User, related_name="user_bet")
    score_host = models.PositiveSmallIntegerField()
    score_away = models.PositiveSmallIntegerField()
    goalscorer = models.ForeignKey(Player, related_name="goalscorer")