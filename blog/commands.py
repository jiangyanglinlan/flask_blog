import click

from .extensions import db


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='生成分类, 默认数量为 10.')
    @click.option('--post', default=50, help='生成文章, 默认数量为 50.')
    @click.option('--comment', default=200, help='生成评论, 默认数量为 200.')
    def forge(category, post, comment):
        from .fakes import fake_admin, fake_categories, fake_posts, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('创建管理员...')
        fake_admin()

        click.echo(f'生成 {category} 条分类...')
        fake_categories(category)

        click.echo(f'生成 {post} 篇文章...')
        fake_posts(post)

        click.echo(f'生成 {comment} 条评论...')
        fake_comments(comment)

        click.echo('Done...')