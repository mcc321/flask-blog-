from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import  Required,Email
from flask_wtf import FlaskForm
from flask_login import UserMixin , current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime


class Login_Form(FlaskForm):
    username=StringField('username',validators=[Required()])
    password=PasswordField('password',validators=[Required()])
    submit=SubmitField('Login')
    def mcc_validate(self):
        if self.username and self.password:
            return True
        else:
            return False


class Register_Form(FlaskForm):
    username=StringField('username',validators=[Required()])
    password=PasswordField('password',validators=[Required()])
    re_password=PasswordField('re_password',validators=[Required()])
    email=StringField('email',validators=[Required()])
    submit=SubmitField('submit')
    def mcc_validate(self):
        if self.username and self.password:
            return True
        else:
            return False

class User(UserMixin,db.Model):
    __tablename__='user'
    __table_args__={'mysql_charset':'utf8'}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30),unique=True)
    password = db.Column(db.String(30),unique=True)
    email = db.Column(db.String(30),unique=False)
    pri = db.Column(db.Integer,default = 1)
    confirmed = db.Column(db.Boolean,default=False)  
    articles = db.relationship('Article',backref='user')

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return False
 
    def is_actice(self):
        return True
 
    def is_anonymous(self):
        return False

    def is_admin(self):
        if self.name=='root':
            return True
        else:
            return False 
    
    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})

    @staticmethod
    def check_activate_token(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data['id'])
        if not user:
            # 用户已被删除
            return False
        # 没有激活时才需要激活
        if not user.confirmed:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
        return True

class Article(UserMixin,db.Model):
    __tablename__ = 'article'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    writer = db.Column(db.String(30),db.ForeignKey('user.name'))
    title = db.Column(db.String(30))
    article = db.Column(db.Text,nullable=True)
    date = db.Column(db.DateTime,default = datetime.datetime)