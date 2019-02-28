from .. import db
from ..models import User , Article,Comment
#----------------------------------------------------------------------------------------------------
#测试使用
#----------------------------------------------------------------------------------------------------
#产生假用户
def userFake(count=100,pri=2,confirmd=True):#默认人数100，默认权限2,通过验证
    from sqlalchemy.exc import IntegrityError
    from random import seed
    import forgery_py

    seed()
    for i in range(count):
        u=User(
            name=forgery_py.name.full_name(),
            password=forgery_py.lorem_ipsum.word(),
            email=forgery_py.internet.email_address(),
            pri=pri,
            confirmed=confirmd
        )
        # print(u.name,u.password,u.email)
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

#产生假文章
def articleFake(count=100):
    from random import seed,randint
    import forgery_py

    seed()
    user_count=User.query.count()
    for i in range(count):
        u=User.query.offset(randint(0,user_count-1)).first()
        a=Article(
            writer=u.name,
            title=forgery_py.lorem_ipsum.word(),
            content=forgery_py.lorem_ipsum.sentences(randint(1,3)),
            date=forgery_py.date.date(True),
            user=u
        )
        db.session.add(a)
        try:
            db.session.commit()
        except:
            db.session.rollback()

def commentFake(count=450):
    from random import seed,randint
    import forgery_py
    seed()
    user_count=User.query.count()
    article_count=Article.query.count()
    for i in range(count):
        u=User.query.offset(randint(0,user_count-1)).first()
        a=Article.query.offset(randint(0,article_count-1)).first()
        c=Comment(
            body=forgery_py.lorem_ipsum.sentences(randint(1,2)),
            date=forgery_py.date.date(True),
            writer_id=u.id,
            article_id=a.id,
            user=u,
            article=a
        )
        db.session.add(c)
        try:
            db.session.commit()
        except:
            db.session.rollback()

#----------------------------------------------------------------------------------------------------