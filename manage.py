import os 
from app import create_app , db
from app.models import User , Article , Comment , Role ,Permission
from flask_script import Manager , Shell,Server
from flask_migrate import Migrate , MigrateCommand
from flask import redirect,url_for,render_template
import click
from flask_cors import CORS
import logging

app = create_app()
CORS(app)
manager = Manager(app)
migrate = Migrate(app,db)#数据库迁移
logging.getLogger('flask_cors').level = logging.DEBUG

def make_shell_context():
    return dict(app = app , db = db , User = User , Role=Role ,  Article = Article , Comment=Comment,Permission=Permission)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)
manager.add_command("server", Server(host='127.0.0.1', port=5000))



@app.route('/')
def root_path():
     return render_template('index.html')

@app.route('/<path:path>',methods=['GET'])
def any_root_path(path):
    return render_template('index.html')

# @app.cli.command()
# @click.option('--drop',is_flag=True,help='Create after drop')
# def initdb(drop):
#      if drop:
#           click.confirm('continue drop?',abort=True)
#           db.drop_all()
#           click.echo('drop tables')
#      db.create_all()
#      click.echo('init')

if __name__ == "__main__":
    manager.run()
    # app.run(host='192.168.137.58',port='5000',debug=True)
