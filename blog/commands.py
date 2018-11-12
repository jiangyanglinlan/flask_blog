import click

from .extensions import db
from .models import Admin


def register_commands(app):
    @app.cli.command()
    @click.option('--username', prompt=True, help='管理员用户名')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='管理员密码')
    @click.option('--category', default=10, help='生成分类, 默认数量为 10.')
    @click.option('--post', default=50, help='生成文章, 默认数量为 50.')
    @click.option('--comment', default=200, help='生成评论, 默认数量为 200.')
    def forge(username, password, category, post, comment):
        from .fakes import fake_admin, fake_categories, fake_posts, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('创建管理员...')
        fake_admin(username, password)

        click.echo(f'生成 {category} 条分类...')
        fake_categories(category)

        click.echo(f'生成 {post} 篇文章...')
        fake_posts(post)

        click.echo(f'生成 {comment} 条评论...')
        fake_comments(comment)

        click.echo('Done...')

    @app.cli.command()
    @click.option('--username', prompt=True, help='管理员用户名')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='管理员密码')
    def init(username, password):
        from .fakes import fake_admin
        click.echo('创建数据库...')
        db.create_all()

        admin = Admin.query.first()
        if admin:
            click.echo('已经存在管理员, 更新数据库中...')
            admin.username = username
            admin.set_password(password)
            db.session.commit()
        else:
            click.echo('创建管理员信息...')
            fake_admin(username, password)
        click.echo('Done...')