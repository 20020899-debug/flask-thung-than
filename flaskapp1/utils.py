import re
from flask import request

def fm(v):
    return f"{v:,.2f}"

def get_float(name, default=0):
    try:
        return float(request.form.get(name, default) or default)
    except:
        return default

def get_eval(name):
    text = request.form.get(name, "").strip()

    if not text:
        return 0

    if not re.match(r'^[0-9+\-*/(). ]+$', text):
        return 0

    try:
        return eval(text)
    except:
        return 0