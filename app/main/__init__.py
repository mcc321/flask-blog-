from flask import render_template , Blueprint




__all__ = []



main = Blueprint('main' , __name__ , template_folder='templates' , static_folder='static')
from . import views




