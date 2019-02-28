
from functools import wraps
from flask import request , current_app ,redirect , url_for
from flask_login import current_user


app=current_app._get_current_object()






@app.template.filter
def capitalize_text(text):
    """convert string to all capitalize"""
    return text.capitalize()                        






