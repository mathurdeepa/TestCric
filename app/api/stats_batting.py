from __future__ import unicode_literals
from django.template.defaultfilters import floatformat
from cricket.core.views.api import BaseStatsView

class View(BaseStatsView):
    ''' 
        wk - week
        mth - month
        sn - season (finish on 31st December )
    '''
    abstract = False
    order_by_options = [
        'name', 'games',  'runs', 'par_runs',
        'highscore',
    ]

    order_by_functions = {
        'name': lambda a, b, c: a.order_by('player_name'),
        'games': lambda a, b, c: sorted(a, key=lambda d: d.get_games(b, c), reverse=True),
        'runs': lambda a, b, c: sorted(a, key=lambda d: d.get_runs(b, c), reverse=True),
        'par_runs': lambda a, b, c: sorted(a, key=lambda d: d.get_par_runs(b, c), reverse=True), 
        'highscore': lambda a, b, c: sorted(
            a,
            key=lambda d: d.get_high_score(b, c),
            reverse=True
        ),
    }

    def filter_function(self, player, years, teams):
        return player.has_batted(years, teams)

    def important_info(self, player, year, team):
        return {
            'player_name': player.player_name,
            'games': player.get_games(year, team),
            'runs': player.get_runs(year, team),
            'par_runs': player.get_par_runs(year, team),
            'high_score': player.get_high_score(year, team),
            'runs_50s': player.get_50s(year, team),
            'runs_100s': player.get_100s(year, team),
        }
