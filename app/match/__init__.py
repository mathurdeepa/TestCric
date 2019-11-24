from __future__ import unicode_literals

from app.match.generic import View as BaseView
from app.match.index import View as Index
from app.match.fixtures import View as Fixtures
from app.match.results import View as Results
from app.match.match import View as Match


__all__ = [
    'BaseView',
    'Index',
    'Fixtures', 'Results',
    'Match',
]
