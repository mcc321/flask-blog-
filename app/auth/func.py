import re
from flask_mail import Message
from flask import request , render_template , flash , jsonify ,current_app
from .. import mail 
from flask_login import current_user


def mail_auth(mail):
    p = re.compile('^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
    x =  p.match(mail)
    if x != None:
        return True
    else:
        return False





def send_mail(receivers,subject,annex,**kwargs):
    app = current_app._get_current_object()
    message=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['MAIL_USERNAME'],recipients=[receivers])
    with app.app_context():
        if 'username' in kwargs:
            message.body=render_template('user.txt',username=kwargs['username'])
            if 'token' in kwargs:
                message.html=render_template('activate.html',token=kwargs['token'],username=kwargs['username'])
    if annex == None:
        with app.app_context():
            mail.send(message)
    else:
        with app.app_context():
            with app.open_resource(annex) as f:
                array=re.split(r'[.,/]',annex)
                type=array[-1]
                if type=='jpg' or type=='bmp' or type=='gif' or type=='bmp' or type=='png':
                    message.attach(annex,'image/'+type,f.read())
                elif type=='mp4' or type=='mkv' or type=='avi':
                    message.attach(annex,'vedio'+type,f.read())
                elif type=='doc' or type=='docx' or type=='txt' or type=='xls' or type=='pptx' or type=='ppt' :
                    message.attach(annex,'doc/'+type,f.read())
                else:
                    pass
                mail.send(message)