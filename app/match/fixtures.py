# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from app.match import BaseView


class View(BaseView):
    def get(self, request):
        self.clear_context()
        self.add_context(
            'matches',
            self.get_fixtures()
        )
        return render(
            request,
            'app/match/fixtures.html',
            context=self.get_context()
        )
