from . import main
from ..func import *
from .func import *
from ..models import User , Login_Form , Register_Form , Article , Comment , Permission,CommentForm,Role
from flask_login import login_required , current_user
from flask import url_for,redirect,jsonify,render_template , current_app
import sys
from ..auth.func import *
from ..util.wraps import *









#-----------------------------------------------通用模块------------------------------------------------
@main.app_context_processor
def inject_permission():
    # 实例化Permission类，并将其字典化
    return dict(Permission=Permission)




# @main.route('/',methods=['POST','GET'])
# def index():
#     from ..auth import auth
#     return render_template('ForWindowsIndex.html')


# @main.route('/<path:path>',methods=['GET','POST'])
# def any_root_path(path):
#     return render_template('index.html')



# @main.route('/fake')
# def makeFake():
#     # userFake(10)
#     articleFake(10)
#     commentFake(30)
#     return "success"



#--------------------------------博文操作模块--------------------------------------------------
@main.route('/blog_article_r',methods=['POST','GET'])
def blog_article_r():
    dic=json_loads()
    if 'id' in dic:
        if db_article_auth(dic['id']):
            article=Article.query.filter_by(id=dic['id']).first()
            user=User.query.filter_by(name=article.writer).first()
            if current_user.pri>=user.pri:
                dic=make_json_dic(200,article_id=article.id,article_content=article.content,article_writer=article.writer,date=article.date)
                return jsonify(dic)
            else:
                dic=make_json_dic(402,article_id=article.id,article_content=article.content,article_writer=article.writer,date=article.date)
                return jsonify(dic)
        else:        
            dic=make_json_dic(404)
            return jsonify(dic)
    else:
        dic=make_json_dic(402)
    return jsonify(dic)





@main.route('/admin/blog_article_w',methods=['POST','GET'])
@login_required
def blog_article_w():
    if current_user.is_authenticated:
        dic=json_loads()
        if 'title' in dic and 'content' in dic:
            article=Article(writer=current_user.name,title=dic["title"],content=dic["content"],date=datetime.datetime.utcnow(),user_id=current_user.id)
            db.session.add(article)
            db.session.commit()
            dic2=make_json_dic(200)
            return jsonify(dic2)
        else:
            dic2=make_json_dic(402)
            return jsonify(dic2)
    else:
        dic2=make_json_dic(402)
        return jsonify(dic2)



#修改博文
@main.route('/admin/blog_article_m',methods=['POST','GET'])
@login_required
def blog_article_m():
    dic=json_loads()
    article=Article.query.filter_by(id=dic['id']).first()
    if current_user.name==article.writer or current_user.role.name=="Adminstrator":
        article.title=dic["title"]
        article.content=dic["content"]
        db.session.add(article)
        db.session.commit()
        dic2=make_json_dic(200)
        return jsonify(dic2)
    else:
        dic2=make_json_dic(303,info="权限不够")
        return jsonify(dic2)

#删除博文
@main.route("/admin/blog_article_d",methods=['POST','GET'])
@login_required
def blog_article_d():
        dic=json_loads()
        article=Article.query.filter_by(id=dic["id"]).first()
        if current_user.name==article.writer or current_user.role.name=="Adminstrator":
            db.session.delete(article)
            db.session.commit()
            dic2=make_json_dic(200)
            return jsonify(dic2)
        else:
            dic2=make_json_dic(303,info="权限不够")
            return jsonify(dic2)





#加载博文列表
@main.route("/admin/blogList",methods=['POST','GET'])
def loadBlogList():
    # current=request.args.get('current',1,type=int)
    # pagesize=request.args.get('pagesize',10,type=int)
    j_data=json_loads()
    mcc_print(j_data)
    current=j_data["current"]
    pagesize=j_data["pagesize"]
    mcc_print(current)
    #查询得到pagination对象
    pagination=Article.query.order_by(Article.date.desc()).paginate(
        page=current,
        per_page=pagesize,
        error_out=False
    )
    #提取博文
    articles=pagination.items
    #提取上一页链接
    prev=None
    if pagination.has_prev:
        prev=url_for("main.loadBlogList",page=current-1,_external=True)
    #提取上一页链接
    next=None
    if pagination.has_next:
        next=url_for("main.loadBlogList",page=current+1,_external=True)
    
    return jsonify({
        "articles":[article.to_jsonList() for article in articles],
        "prev":prev,
        "next":next,
        "total":pagination.total#记录总数
    })

#加载文章
@main.route("/admin/article")
def loadArticle():
    id=request.args.get("id",1,type=int)#从url中获取id
    article=Article.query.filter_by(id=id).first()
    if(article):
        j_data=article.to_jsonArticle()
        j_data["statusCode"]=200
        return jsonify(j_data)
    else:
        dic2=make_json_dic(404)
        return jsonify(dic2)

#加载所有的用户
@main.route("/admin/userlist",methods=['POST','GET'])
@login_required
@admin_required
def getUser():
    get_data=json_loads()
    current=get_data["current"]
    pagesize=get_data["pagesize"]
    pagination=User.query.paginate(current,pagesize)
    users=pagination.items
    return jsonify({
        "users":[user.to_json() for user in users],
        "total":pagination.total,
        "statusCode":200
    })

#提升一个用户的权限为管理员
@main.route("/admin/upgrade",methods=['POST'])
@admin_required
def upgradePermission():
    get_data=json_loads()
    id=get_data["id"]
    user=User.query.filter_by(id=id).first()
    if(user.role.name !="Adminstrator"):
        user.pri=2
        user.role.name=="Adminstrator"
        user.role_id=Role.query.filter_by(name="Adminstrator").first().id
        db.session.add(user)
        db.session.commit()
        return jsonify(make_json_dic(200,info="提升成功"))
    else:
        return jsonify(make_json_dic(303,info="该用户已经是管理员"))

#删除用户
@main.route("/admin/delete",methods=['POST'])
@admin_required
def deleteUser():
    get_data=json_loads()
    id=get_data["id"]
    user=User.query.filter_by(id=id).first()
    if user.role.name=="Adminstrator":
        return jsonify(make_json_dic(301,info="无法删除管理员"))
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify(make_json_dic(200))

#加载一个用户的所有文章
@main.route("/admin/user/<int:user_id>",methods=['POST','GET'])
@login_required
def getUserArticle(user_id):
    if(user_id==0):
        user_id=current_user.id
    get_data=json_loads()
    current=get_data["current"]
    pagesize=get_data["pagesize"]
    # pagination=Article.query.filter_by(user.id=user_id).order_by(Article.date.desc()).paginate(
    #     current,pagesize
    # )
    user=User.query.filter_by(id=user_id).first()#查询用户
    pagination=user.article.order_by(Article.date.desc()).paginate(current,pagesize)#分页查博文
    articles=pagination.items
    return jsonify({
        "articles":[article.to_jsonList() for article in articles],
        "total":pagination.total,
        "statusCode":200
    })
#--------------------------------------------------------评论模块-------------------------------------------------------------------------------------------
# 关于评论模块分为三部分，第一部分为普通用户或匿名用户评论模块如果是普通用户则允许写评论
# 的第二部分为article的预览模块路由
# 第三部分为每个article的评论管理模块，管理员可以评论，也可以删除评论


from ..util.wraps import login_required 
#commment模块即可以添加评论，又可以分页显示评论
@main.route('/article_comment/<int:id>',methods=['GET','POST'])
def article_comment(id):
    article=Article.query.filter_by(id=id).first()
    form = CommentForm()
    #发表评论模块
    if form.body.data:
        mcc_print(form.body)
        if current_user.is_authenticated:
            comment=Comment(body=form.body.data,article=article,user=current_user._get_current_object())
            mcc_print(comment.body)
            db.session.add(comment)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            db_comment=Comment.query.filter_by(body=form.body.data).first()
            # return redirect(url_for('main.article',id=article.id,page=-1))
            # dic=make_json_dic(200,comment_id=db_comment.id,body=form.body.data,article_title=article.title,date=datetime.datetime.utcnow(),writer=current_user._get_current_object().name,comment_pagination=pagination)
            dic=make_json_dic(200)
            return jsonify(dic)
        else:
            dic=make_json_dic(301,info="登陆查看评论")
            return jsonify(dic)

    # #删除评论模块
    # info=json_loads()
    # if info.comment_id.data:
    #     comment=Comment.query.filter_by(id=form.comment_id.data).first()
    #     if current_user._get_current_object()==comment.user:
    #         if info['del']==True and info['comment_id'] is not None and info['re_del']==True:
    #             comment = Comment.query.filter_by(id=info['comment_id']).first()
    #             db.session.delete(comment)
    #             dic=make_json_dic(200)
    #             return dic
    #         else:
    #             dic=make_json_dic(304)
    #             return dic
    #     else:
    #         dic=make_json_dic(305)
    #         return dic
    # else:
    #     dic=make_json_dic(305)
    #     return dic

                

    #分页显示模块
    info_data=json_loads()
    current=info_data["current"]
    pagesize=info_data["pagesize"]
    
    pagination=Comment.query.filter_by(article_id=id).order_by(Comment.date.desc()).paginate(
        page=current,
        per_page=pagesize,
        error_out=False
    )
    prev=None
    if pagination.has_prev:
        prev=url_for('main.article_comment' ,id=id ,page= current-1, _external=True)
    next=None
    if pagination.has_next:
        next=url_for('main.article_comment' , id=id,page=current+1,_external=True)
    comments = pagination.items
    # return render_templtate('article.html',article=[article],form=form,comment=comment,pagination=pagination)
    dic=make_json_dic(200,comment=[comment.to_json_comment() for comment in comments],prev=prev,next=next,total=pagination.total)
    return jsonify(dic)
    




# 管理评论
@main.route('/admin/article')    
@login_required
def admin_article():
    if current_user.is_admin():
        info_data=json_loads()
        current=request_data["current"]
        pagesize=request_data["pagesize"]
        
        pagination=Article.query.order_by(Article.date.desc()).paginate(
            page=current,
            per_page=pagesize,
            error_out=False
        )
        if pagination.has_prev:
            prev=url_for('main.admin_article' , page= current-1, _external=True)
        next=None
        if pagination.has_next:
            next=url_for('main.admin_article' , page=current+1,_external=True)
        comments = pagination.items
        dic=make_json_dic(200,comment=[comments.to_json_comment() for comment in comments],prev=prev,next=next,total=pagination.total)
        return jsonify(dic)
    else:
        dic=make_json_dic(301)
        return jsonify(dic)


    


@main.route('/admin/article_comment/<int:id>',methods=['POST'])    
@login_required
def admin_article_comment(id):
    if current_user.is_admin():
        #删除评论模块
        article=Article.query.filter_by(id=id).first()
        comment=Comment.query.filter_by(article=article).first()
        info=json_loads()
        if info['del']==True and info['comment_id'] is not None and info['re_del']==True:
            comment = Comment.query.filter_by(id=info['comment_id']).first()
            db.session.delete(comment)
            dic=make_json_dic(200)
            return dic
        #发表评论模块
        form = CommentForm()
        if form.mcc_validate():
            comment=Comment(body=form.body.data,article=article,writer=current_user._get_current_object().user.name)
            db.session.add(comment)
            db.session.commit()
            # return redirect(url_for('main.article',id=article.id,page=-1))
            dic=make_json_dic(200,body=form.body.data,article_title=article.title,date=datetime.datetime.utcnow,writer=current_user.get_current_object().user.name,comment_pagination=pagination)
            return jsonify(dic)
        #分页显示模块
        current=request_data["current"]
        pagesize=request_data["pagesize"]
        
        pagination=Comment.query.order_by(Comment.date.desc()).paginate(
            page=current,
            per_page=pagesize,
            error_out=False
        )
        prev=None
        if pagination.has_prev:
            prev=url_for('main.admin_article_comment' ,id=id, page=current-1, _external=True)
        next=None
        if pagination.has_next:
            next=url_for('main.admin_article_comment' ,id=id, page=current+1,_external=True)
        comments = pagination.items
        dic=make_json_dic(200,comment=[comment.to_json_comment() for comment in comments],prev=prev,next=next,total=pagination.total)
        return jsonify(dic)
    else:
        dic=make_json_dic(301)
        return dic







@main.route('/test')
@login_required
def user():
    if current_user.is_authenticated:
        return jsonify(name=current_user._get_current_object().name)
    else:
        return jsonify(name='none')
































#-----------------------------------------------测试模块---------------------------------------------------

@main.route('/test')
@login_required
def test():
    mcc_print('login')
    return render_template('ForWindowsIndex.html')



