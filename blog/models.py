from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .extensions import db


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about= db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', backref='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan')
    can_comment = db.Column(db.Boolean, default=True)

    def reviewed_comments(self):
        return [comment for comment in self.comments if comment.reviewed is True]


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)  # 是否来自管理者
    reviewed = db.Column(db.Boolean, default=False)  # 是否通过审核
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    replied_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    replies = db.relationship('Comment', backref=db.backref('replied', remote_side=[id]),
                              cascade='all, delete-orphan')


