from . import auth
from flask import render_template , url_for, session, redirect

from ..models import User , Login_Form , Register_Form , Article 
from flask_login import current_user , login_required , login_user , logout_user , user_logged_in
from ..func import *
from .func import *




@auth.route('/')
def index():
    return render_template('index.html')

@auth.route('/<path:path>',methods=['GET','POST'])
def any_root_path(path):
    return render_template('index.html')

# @auth.route('/register',methods=['POST'])
# def registerId():
#     if current_user.is_authenticated:
#         dic=make_json_dic(301,name='annoyance',date=mcc_time(),info=mcc_info('you have already authenticated.'))
#         return jsonify(dic)
#     else:
#         if request.method=='POST':
#             form=Register_Form()
#             if form.mcc_validate():
#             #if form.validate_on_submit():
#                 name=form.username.data
#                 if form.password.data==form.re_password.data:
#                     password=form.password.data
#                     email=form.email.data               
#                     if db_user_auth(name,password)==False:
#                         if mail_auth(email):
#                             user=User()
#                             user.name=name
#                             user.password=password
#                             user.email=email
#                             user.__init__()
#                             db.session.add(user)
#                             db.session.commit()
#                             token = user.generate_activate_token()
#                             # 发送激活邮件到注册邮箱
#                             send_mail(email, '账户激活', 'auth\\templates\\Life_Is_Strange_Artwork_5.jpg', token=token,username=name)
#                             # 提示用户下一步操作
#                             dic=make_json_dic(200)
#                             return jsonify(dic)
#                         else:
#                             dic=make_json_dic(301,user_username=name,date=mcc_time(),info=mcc_info('email type erro.'))
#                             return jsonify(dic)
#                             #return redirect(url_for('main.register'))
#                         # user=User()
#                         # user.name=name
#                         # user.password=password
#                         # user.email=email
#                         # user.pri=1
#                         # user.confirmed=False
#                         # mcc_print(user.name)
#                         # db.session.add(user)
#                         # db.session.commit()
#                         # try:
#                         #     db.session.commit()
#                         # except:
#                         #     db.session.rollback()
#                         # return jsonify(make_json_dic(200))
#                     else:
#                         dic=make_json_dic(301,user_username=name,date=mcc_time(),info=mcc_info('the user is registered .'))
#                         return jsonify(dic)
#                         # return render_template('register.html')
#                 else:
#                     dic=make_json_dic(301,user_username=name,date=mcc_time(),info=mcc_info('the password is not same.'))
#                     return jsonify(dic)
#                     # return render_template('register.html')
#             else:
#                 dic=make_json_dic(301,user_username=name,date=mcc_time(),info=mcc_info('the form is not complete. '))
#                 return jsonify(dic)
#                 # return render_template('register.html')
#         else:
#             dic=make_json_dic(301,date=mcc_time(),info=mcc_info('the request is not supported.'))
#             return jsonify(dic)
#             # return render_template('register.html')
@auth.route('/register',methods=['POST'])
def registerId():
    if current_user.is_authenticated:
        dic=make_json_dic(301,name='annoyance',date=mcc_time(),info=mcc_info('you have already authenticated.'))
        return jsonify(dic)
    else:
        if request.method=='POST':
            form=Register_Form()
            if form.mcc_validate():
            #if form.validate_on_submit():
                name=form.username.data
                if form.password.data==form.re_password.data:
                    password=form.password.data
                    email=form.email.data               
                    if db_user_auth(name,password)==False:
                        if mail_auth(email):
                            user=User()
                            user.name=name
                            user.password=password
                            user.email=email
                            user.role_id=1
                            db.session.add(user)
                            db.session.commit()
                            token = user.generate_activate_token()
                            # 发送激活邮件到注册邮箱
                            send_mail(email, '账户激活', 'auth\\templates\\Life_Is_Strange_Artwork_5.jpg', token=token,username=name)
                            # 提示用户下一步操作
                            dic=make_json_dic(200)
                            return jsonify(dic)
                        else:
                            dic=make_json_dic(301,user_username=name,date=mcc_time(),info=mcc_info('email type erro.'))
                            return jsonify(dic)
                            #return redirect(url_for('main.register'))
                        # user=User()
                        # user.name=name
                        # user.password=password
                        # user.email=email
                        # user.pri=1
                        # user.confirmed=False
                        # mcc_print(user.name)
                        # db.session.add(user)
                        # db.session.commit()
                        # try:
                        #     db.session.commit()
                        # except:
                        #     db.session.rollback()
                        # return jsonify(make_json_dic(200))
                    else:
                        dic=make_json_dic(301,user_username=name,date=mcc_time(),info=mcc_info('the user is registered .'))
                        return jsonify(dic)
                        # return render_template('register.html')
                else:
                    dic=make_json_dic(301,user_username=name,date=mcc_time(),info=mcc_info('the password is not same.'))
                    return jsonify(dic)
                    # return render_template('register.html')
            else:
                return jsonify(make_json_dic(306,info="用户邮箱已注册"))
        else:
            return jsonify(make_json_dic(304,info="用户名称已注册"))


@auth.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        mcc_print("you are authenticated")
        dic=make_json_dic(200,user_username=current_user._get_current_object().name,date=mcc_time(),info='current user is authenticated.')
        return jsonify(dic)    
    else:       
        form=Login_Form()
        dic=form_analysis(form)
        if dic!=None:
            if request.method=='POST':
                username=dic['username']
                password=dic['password']
                user=User.query.filter_by(name=username).first()
                mcc_print(user)
                if user:
                    if user is not  None and password==user.password and user.confirmed==True:
                        session["username"]=username
                        session["password"]=password
                        login_user(user,True)
                        # dic=make_json_dic(200,user_username=current_user.name,date=mcc_time(),info=mcc_info('current user is login.'))
                        # dic=make_json_dic(200,user_username=current_user.name,info=mcc_info('current user is login.'))
                        dic=make_json_dic(200,is_admin=(user.role.name=="Adminstrator"))
                        return jsonify(dic)          
                    else:
                        # dic=make_json_dic(301,user_username=current_user.name,date=mcc_time(),info=mcc_info('authenticate fail.'))
                        dic=make_json_dic(301,info='账号密码错误或邮箱未激活')
                    return jsonify(dic)
                else:
                    return jsonify(make_json_dic(304,info="用户名不存在"))
            else:
                dic=make_json_dic(301,info='请求方式错误')
                return jsonify(dic)
        else:
            dic=make_json_dic(404,info='表格不完整')

            return jsonify(dic)

@auth.route('/islogin',methods=["GET"])
def getState():
    if current_user.can(0x01):
        j_data=make_json_dic(200,user_username=current_user._get_current_object().name,user_id=current_user._get_current_object().id,is_admin=(current_user.role.name=="Adminstrator"))
        return jsonify(j_data)
    else:
        j_data=make_json_dic(303)
        return jsonify(j_data)


@auth.route('/logout',methods=['POST','GET'])
def logout():
    if current_user.is_authenticated:
        dic=make_json_dic(200,user_username=current_user._get_current_object().name,date=mcc_time(),info=mcc_info('logout success.'))
        logout_user()
        return jsonify(dic)
        # return render_template('index.html')
    else:
        # dic=make_json_dic(301,user_username=current_user._get_current_object().name,date=mcc_time(),info=mcc_info('you have login.'))
        dic=make_json_dic(301)
        return jsonify(dic)
        # return render_template('login.html')

@auth.route('/activate/<token>')
def activate(token):
    if token !=None:
        if User.check_activate_token(self=current_user,token=token):
            dic=dict()
            dic['info']='activate success'
            return redirect(url_for('auth.login'))
        else:
            dic=dict()
            dic['info']='activate fail'
            return redirect(url_for('auth.index'))
    else:
        mcc_print('none')

#用户修改自己的姓名或者密码
