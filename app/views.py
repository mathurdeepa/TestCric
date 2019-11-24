"""
Definition of views.
"""
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.generic import *
from app.exceptions import *
from app.models import *
from django.shortcuts import render
from django.db.models import Min
 
def get_teams():
    return Team.objects.filter(club__home_club=True).order_by('name')

def index(request):
    players = Player.objects.filter(club__home_club=True).all()
    top_run_scorers = sorted(players, key=lambda a: a.get_runs())[:-6:-1]
    top_run_scorers = filter(lambda a: a.get_runs() is not None, top_run_scorers)
    return render(
        request,
        'app/stats/index.html',
        context={
            'top_run_scorers': top_run_scorers,
        }
    )

def batting(request):
    players = Player.objects.filter(club__home_club=True)
    players = reversed(sorted(players, key=lambda a: a.get_runs()))
    final_players = []
    for i in players:
        if i.has_batted():
            final_players.append(i)
    return render(
        request,
        'app/stats/batting.html',
        context={
            'players': final_players[:20],
            'teams': get_teams(),
        }
    )



class View(ArgumentView):

    def validate_match_id(self, match_id):
        match = get_object_or_404(Match, id=match_id)
        self.add_context('match', match)
        if not match.full_scorecard and match.processing_issue:
            raise kwargError('Match has not got a scorecard')
        if match.result in ['A', 'C', 'CON']:
            raise kwargError('Match was not played')

    def get_context_value(self, key):
        if key not in self.context.keys():
            raise KeyError('Key not in context')
        return self.context[key]

    
    def get_role(self):
        match = self.get_context_value('match')
        bat_role = BatPerformance.objects.filter(match__id=match.id)
  
    def get(self, request, **kwargs):
        self.clear_context()
        try:
            self.validate_kwargs()
       
            self.get_role()
            return render(
                request,
                'app/stats/match.html',
                context=self.get_context()
            )
        except kwargError:
            return render(
                request,
                'app/stats/notplayed.html',
                context=self.get_context()
            )
         