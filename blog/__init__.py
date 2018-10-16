import os

from flask import Flask

from .blueprints.admin import admin_bp
from .blueprints.auth import auth_bp
from .blueprints.blog import blog_bp
from .extensions import bootstrap, db, migrate, moment
from .settings import config
from .commands import register_commands
from .models import Admin, Category, Post

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

        app = Flask('blog')
        app.config.from_object(config[config_name])

        register_extensions(app)  # 注册扩展(扩展初始化)
        register_blueprints(app)  # 注册蓝本
        register_commands(app)  # 虚拟数据
        register_template_context(app)  # 处理模板上下文
        return app


def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)