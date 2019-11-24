from __future__ import unicode_literals
from django.http import JsonResponse
from django.views.generic import View as V
from app.exceptions import *

class View(V):
    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)

    def get_kwarg(self, key, default=None):
        try:
            return self.kwargs[key]
        except KeyError:
            return default

    def JsonResponse(self, data={}):
        return JsonResponse(
            {
                'error': False,
                'data': data,
            }
        )

    def error_message(self, message=""):
        return JsonResponse(
            {
                'error': True,
                'message': message,
            }
        )

    def validate_kwargs(self):
        kwargs = self.kwargs
        for k, v in kwargs.iteritems():
            func_name = 'validate_{}'.format(k)
            if func_name in dir(self):
                f = getattr(self, func_name)
                if callable(f):
                    f(v)
                else:
                    raise validateFunctionNotCallable