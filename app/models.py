from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import  Required,Email
from flask_wtf import FlaskForm
from flask_login import UserMixin , current_user , AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,jsonify
import datetime
from . import db , login_manager
import bleach
from markdown import markdown



#Login_manager回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler#处理未登录情况
def unauthorized_handler():
    return jsonify({
        "statusCode":404
    })


#表单类
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
        if self.username.data and self.password.data:
            return True
        else:
            return False




class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('Submit')




#数据库类

#权限位表
class Permission:
    """
    权限表
    """
    # COMMENT = 0x01  # 查看评论
    COMMENT = 0x01  # 查看评论
    ARTICLES = 0x02 #管理自己的文章,添加评论
    ADMINISTER=0x07 #管理全部文章



class User(UserMixin,db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30),unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(30),unique=False)
    pri = db.Column(db.Integer,default = 1)
    confirmed = db.Column(db.Boolean,default=False)  
    article = db.relationship('Article',backref='user', lazy='dynamic',cascade='save-update,delete,merge')
    comment = db.relationship('Comment',backref = 'user', lazy='dynamic',cascade='save-update,delete,merge')
    role_id = db.Column(db.Integer , db.ForeignKey('role.id'))

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        # if self.role is None:
        #     if self.email ==current_app.config['FLASKY_ADMIN']:
        #         self.role=Role.query.filter_by(permissions=0x0D).first()
        if self.role is None:
            self.role=Role.query.filter_by(default=True).first()

    def is_admin(self):
        if self.name=='root':
            return True
        else:
            return False 

    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})
    def to_json(self):
        j_data={
            "id":self.id,
            "name":self.name
        }
        return j_data
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

    def can(self,permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # @staticmethod
    # def can(self , method):
    #     if self.pri >= method:
    #         return True
    #     else :
    #         return False
    
    def get(id):
        user=User.query.filter_by(id=id).first()
        return user
    

   

class AnonymousUser(AnonymousUserMixin):
    name='annoyance'
    id=0
    def can(self, permissions):
        return False
        
    def is_administrator(self):
        return False

#匿名用户
login_manager.anonymous_user = AnonymousUser

class Article(db.Model):
    __tablename__ = 'article'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    writer = db.Column(db.String(30))
    title = db.Column(db.String(30))
    content = db.Column(db.Text,nullable=True)
    date = db.Column(db.DateTime,default = datetime.datetime.utcnow)
    comment = db.relationship('Comment',backref = 'article', lazy='dynamic',cascade='all')
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    def to_jsonList(self):
        json_list={
            "id":self.id,
            "writer":self.user.name,
            "title":self.title,
            "date":self.date
        }
        return json_list
    def to_jsonArticle(self):
        json_article={
            "writer":self.user.name,
            "title":self.title,
            "date":self.date,
            "content":self.content
        }
        return json_article

#角色模型
class Role(db.Model):
    __tablename__='role'
    __table_args__ = {'mysql_charset': 'utf8'}
    #id = db.Column(db.Integer,primary_key=True)
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(64),unique=True)
    permissions=db.Column(db.Integer)
    default=db.Column(db.Boolean,default=False,index=True)#设置注册用户时候的默认角色
    user = db.relationship('User',backref = 'role', lazy='dynamic')


    @staticmethod
    def insert_roles():
        roles={
            "User":(Permission.COMMENT | Permission.ARTICLES,True),
            "Adminstrator":(0x07,False),
            "Annoyance":(0x01,False)
        }
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.permissions=roles[r][0]
            role.default=roles[r][1]
            db.session.add(role)
        db.session.commit()



class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    date = db.Column(db.DateTime , index = True , default = datetime.datetime.utcnow)
    disabled = db.Column(db.Boolean)
    writer_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer , db.ForeignKey('article.id'))

    def to_json_comment(self):
        dic=dict()
        dic['id']=self.id
        dic['body']=self.body
        dic['date']=self.date
        dic['writer']=self.user.name
        dic['article_title']=self.article.title
        return dic
	
    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i','strong']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                            tags=allowed_tags, strip=True))
db.event.listen(Comment.body, 'set', Comment.on_changed_body)
