# -*- coding: utf-8 -*-
# from flask import render_template
# import os , sys
# dir_path = os.path.abspath(os.path.dirname(__file__))
# package_path = os.path.join(dir_path , '..')
# print(package_path)
# sys.path.append(package_path)
# from main import main
from . import main
from flask import render_template


@main.app_errorhandler(404)
def page_not_found():
    return render_template(), 404
 
@main.app_errorhandler(500)
def internal_server_error():
    return render_template(), 500
