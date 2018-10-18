import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from .models import Admin, Category, Post, Comment
from .extensions import db


fake = Faker('zh_CN')


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='上海堡垒',
        blog_sub_title='铁甲依然在',
        name='江洋',
        about='Python web, 作家江南粉, 商人二框黑'
    )
    admin.set_password('flaskblog')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):

    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback() # 若随机生成的分类名重复, 则调用 rollback() 回滚


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()


def fake_comments(count=200):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # 未审核评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # 管理员发表的评论
        comment = Comment(
            author='江洋',
            email='jiangyang@example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    db.session.commit()

    # 回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
        )
        replied = comment.replied
        comment.post = replied.post
        if comment.timestamp < replied.timestamp:
            comment.timestamp, replied.timestamp = replied.timestamp, comment.timestamp
            db.session.add(replied)
        db.session.add(comment)
    db.session.commit()
