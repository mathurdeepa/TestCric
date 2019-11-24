"""
Definition of models.
"""
from django.db import models
from django.db.models import Sum, F, Max, Q
from datetime import date, datetime
import warnings
import pytz

def get_current_year():
    return date.today().year

class MatchDate(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    date = models.DateField()

    def get_date(self):
        return date(self.year, self.month, self.day)

    def get_datetime(self):
        return datetime(self.year, self.month, self.day, 12, 0, 0, 0, pytz.UTC)

    def __str__(self):
        return str(self.year) + '/' + str(self.month) + '/' + str(self.day)

class Club(models.Model):
    name = models.CharField(max_length=255)
    clubState = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Team(models.Model):
    id = models.AutoField(primary_key =True)
    name = models.CharField(max_length=100)
    logoUri = models.ImageField(upload_to ='images/team/')
    clubState = models.ForeignKey('Club', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Scorer(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class MatchName(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    matchName = models.ForeignKey('MatchName', on_delete=models.CASCADE)
    home_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='home_team')
    outer_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='outer_team')
    date = models.ForeignKey('MatchDate', on_delete=models.CASCADE)
    def match_info(self):
        warnings.warn('match_info not setup correctly', UserWarning)
        if True: 
            return self.home_team.name + ' vs ' + self.outer_team.club.name + ' ' + self.outer_team.name
        else:
            return self.outer_team.name + ' vs ' + self.home_team.club.name + ' ' + self.home_team.name

    def opposite_team(self):
        warnings.warn('opposite_team not setup correctly', UserWarning)
        if True: 
            return str(self.outer_team)

        else:
            return str(self.home_team)

class ScorerInfo(models.Model):
    scorer = models.ForeignKey('Scorer', on_delete=models.CASCADE)
    match = models.ForeignKey('Match', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.scorer) + ' - ' + str(self.match)

class Player(models.Model):
    id = models.AutoField(primary_key =True)
    team_id =models.ForeignKey(Team,on_delete = models.CASCADE,blank=True,null =True)
    firstName =models.CharField(max_length =100)
    lastName = models.CharField(max_length =100)
    imageUri = models.ImageField(upload_to = 'image/player/')
    playerJarseryName = models.IntegerField(null = False)
    country = models.CharField(max_length =100)

    def __str__(self):
        return str(self.firstName) + ' ' + self.lastName

    def played_game(self,season=[get_current_year()], teams=[]): 
        return Role.objects.filter(
            Q(match__home_team__id__in=teams) | Q(match__outer_team__id__in=teams),
            player__id=self.id,
            match__date__year__in=season,
        ).count() != 0

    def get_games(self,season=[get_current_year()],teams=[]): 
        return Role.objects.filter(
            Q(match__home_team__id__in=teams) | Q(match__outer_team__id__in=teams),
            player__id=self.id,
            match__date__year__in=season,
        ).count()

    def get_runs(self,season=[get_current_year()],teams=[]): 
        return BatRole.objects.filter(
            Q(match__home_team__id__in=teams) | Q(match__outer_team__id__in=teams),
            player__id=self.id,
            match__date__year__in=season,
            bat=True,
        ).aggregate(Sum('bat_runs'))['bat_runs__sum']

    def get_par_runs(self,season=[get_current_year()],teams=[]): 
        return BatRole.objects.filter(
            Q(match__home_team__id__in=teams) | Q(match__outer_team__id__in=teams),
            player__id=self.id, 
            match__date__year__in=season,
            bat=True,
        ).aggregate(Sum('bat_par_score'))['bat_par_score__sum']

    def get_50s(self,season=[get_current_year()],teams=[]):
        return BatRole.objects.filter(
            Q(match__home_team__id__in=teams) | Q(match__outer_team__id__in=teams),
            player__id=self.id,
            match__date__year__in=season,
            bat=True,
            bat_runs__range=[50, 99],
        ).count()

    def get_100s(self,season=[get_current_year()],teams=[]): 
        return BatRole.objects.filter(
            Q(match__home_team__id__in=teams) | Q(match__outer_team__id__in=teams),
            player__id=self.id,
            match__date__year__in=season,
            bat=True,
            bat_runs__gte=100,
        ).count()

    def get_high_score(self,season=[get_current_year()],teams=[]):  
        return BatRole.objects.filter(
            Q(match__home_team__id__in=teams) | Q(match__outer_team__id__in=teams),
            player__id=self.id,
            match__date__year__in=season,
        ).aggregate(Max('bat_runs'))['bat_runs__max']

class Role(models.Model):
    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.player) + ': ' + str(self.match)

class BatRole(models.Model):
    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    bat_runs = models.IntegerField(default=0)
    bat_par_score = models.IntegerField(default=0)
    def __str__(self):
        return str(self.player) + ': ' + str(self.match)
