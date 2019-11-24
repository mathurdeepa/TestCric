from __future__ import unicode_literals
from app.exceptions import AbstractFunctionError

def abstract_function(func):
    def func_wrapper(*args, **kwargs):
        raise AbstractFunctionError
