from .models import User , Article ,Comment
from . import db,login_manager
from flask import request , render_template , flash , jsonify , current_app
import json , re , time , datetime
from flask_mail import Message
import datetime




#----------------------------------------------------------------
#认证类函数,因为这里容易混淆，所以建议以库名加属性加auth来命名
#----------------------------------------------------------------

def db_user_auth(name,password):
    user=User.query.filter_by(name=name).first()
    if user is not  None and password==user.password:
        return True
    else:
        return False



def db_article_auth(id):
    article=Article.query.filter_by(id=id).first()
    if article is not  None:
        return True
    else:
        return False

def db_comment_auth(id):
    comment=Comment.query.filter_by(id=id).first()
    if comment is not  None:
        return True
    else:
        return False





def db_user_push(dic):
    user=User.query.filter_by(name=dic['name']).first()
    if user is None:
        user=User()
        user.name=dic['name']
        user.password=dic['password']
        user.email=dic['email']
        user.pri=dic['pri']
        user.confirmed=dic['confirmed']
        user.__init__()
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            mcc_print(roll)
        return True
    else:
        return False


def db_article_push(dic):
    article=Article.query.filter_by(title=dic['title']).first()
    if article is None:
        article=Article()
        article.title=dic['title']
        article.writer=dic['writer']
        article.date=dic['date']
        article.content=dic['content']
        db.session.add(article)
        db.session.commit()
        return True
    else:
        return False

def db_article_modify(dic):
    article=db.session.query(Article).filter_by(id=dic["id"]).scalar()
    if article:
        article.date=dic["date"]
        article.writer=dic["writer"]
        article.title=dic["title"]
        article.content=dic["content"]
        try:#处理异常情况
                db.session.commit()
        except:
                db.session.rollback()#异常回滚
        return True
    else:
        return False

def db_article_delete(dic):
    article=Article.query.filter_by(id=dic["id"]).first()
    db.session.delete(article)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


#----------------------------------------------------------------
#使用函数类，自定义的函数放这里，尽量通俗易懂，尽量简单
#----------------------------------------------------------------
def json_loads():
    pre_data=request.get_data().decode('utf-8')
    dic=json.loads(pre_data)
    return dic


#用户提交的表单分析函数
def form_analysis(form):
    if form.mcc_validate():
        if request.method=='POST':
            username=form.username.data
            password=form.password.data
            #如有除username和password的属性，在这里添加
            dic=dict()
            dic['username']=username
            dic['password']=password
            return dic
        else:
            return None
    else:
        return None



def make_json_dic(statusCode,**kwargs):
    mcc=dict()
    mcc['statusCode']=statusCode
    
    #通用模块
    if 'date' in kwargs:
        mcc['date']=kwargs['date']
    if 'info' in kwargs:
        mcc['info']=kwargs['info']
    if 'article' in kwargs:
        mcc['article']=kwargs['article']
    if 'form' in kwargs:
        mcc['form']=kwargs['form']
    if 'pagination' in kwargs:
        mcc['pagination']=kwargs['pagination']
    if 'comment' in kwargs:
        mcc['comment']=kwargs['comment']
    if 'page' in kwargs:
        mcc['page']=kwargs['page']
    if 'body' in kwargs:
        mcc['body']=kwargs['body']
    if 'prev' in kwargs:
        mcc['prev']=kwargs['prev']
    if 'next' in kwargs:
        mcc['next']=kwargs['next']
    if 'total' in kwargs:
        mcc['total']=kwargs['total']

    #用户模块
    if 'user_username' in kwargs:
        mcc['user_username']=kwargs['user_username']
    if 'user_id' in kwargs:
        mcc['user_id']=kwargs['user_id']
    
    
    #article模块
    if 'article_title' in kwargs:
        mcc['article_title']=kwargs['article_title']    
    if 'article_id' in kwargs:
        mcc['article_id']=kwargs['article_id']    
    if 'article_writer' in kwargs:
        mcc['article_writer']=kwargs['article_writer']
    if 'article_content' in kwargs:
        mcc['article_content']=kwargs['article_content']
    if 'article_date' in kwargs:
        mcc['article_date']=kwargs['article_date']
    

    #comment模块
    if 'comment_form' in kwargs:
        mcc['comment_form']=kwargs['comment_form']
    if 'comment_article' in kwargs:
        mcc['comment_article']=kwargs['comment_article']
    if 'comment_pagination' in kwargs:
        mcc['comment_pagination']=kwargs['comment_pagination']
    if 'comment_comment' in kwargs:
        mcc['comment_comment']=kwargs['comment_comment']
    if 'comment_id' in kwargs:
        mcc['comment_id']=kwargs['comment_id']




    return mcc



#弃用，以后时间以datetime.datetime.utcnow来获取
def mcc_time():
    ISOTIMEFORMAT='%Y-%m-%d %X'
    return  datetime.datetime.utcnow()



def mcc_info(info):
    app=current_app._get_current_object()
    app.logger.info(info)
    flash(info)
    return info


def mcc_print(info):
    app=current_app._get_current_object()
    app.logger.info(info)  


def get_app_config(attrib):
    app=current_app._get_current_object()
    return app[attrib]
