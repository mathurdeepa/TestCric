from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from app.generic import ArgumentView
from app.exceptions import kwargError, notEnoughInningsError
from app.models import *


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
        bat_role = BatRole.objects.filter(match__id=match.id)
       

        
 
    def get(self, request, **kwargs):
        self.clear_context()
        try:
            self.validate_kwargs()
            self.get_role()
            return render(
                request,
                'app/matches/match.html',
                context=self.get_context()
            )
        except kwargError:
            return render(
                request,
                'app/matches/notplayed.html',
                context=self.get_context()
            )
        except notEnoughInningsError:
            return render(
                request,
                'app/matches/basic.html',
                context=self.get_context()
            )
