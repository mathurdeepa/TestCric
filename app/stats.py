# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports
from django.shortcuts import render
from django.db.models import Min
from datetime import date
from cricket.core.models import Player, Team, MatchDate


def get_seasons():
    start_year = MatchDate.objects.all().aggregate(Min('year'))['year__min']
    return range(date.today().year, start_year - 1, -1)


def get_teams():
    return Team.objects.filter(club__home_club=True).order_by('name')


def index(request):
    players = Player.objects.filter(club__home_club=True).all()
    top_wicket_takers = sorted(players, key=lambda a: a.get_wickets())[:-6:-1]
    top_wicket_takers = filter(lambda a: a.get_wickets() is not None, top_wicket_takers)
    top_run_scorers = sorted(players, key=lambda a: a.get_runs())[:-6:-1]
    top_run_scorers = filter(lambda a: a.get_runs() is not None, top_run_scorers)
    top_catch_takers = sorted(players, key=lambda a: a.get_catches())[:-6:-1]
    top_catch_takers = filter(lambda a: a.get_catches() is not None, top_catch_takers)
    return render(
        request,
        'app/stats/index.html',
        context={
            'current_season': date.today().year,
            'top_run_scorers': top_run_scorers
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
            'seasons': get_seasons(),
            'teams': get_teams(),
        }
    )

 