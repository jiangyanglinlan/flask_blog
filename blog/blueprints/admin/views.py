from flask import render_template, request, current_app
from flask_login import login_required

from . import admin_bp
from ...models import Post


@admin_bp.before_request
@login_required
def login_protect():
    '''
    为 admin 蓝本下的所有视图函数添加保护
    '''
    pass


@admin_bp.route('/post/manage')
@login_required
def manage_post():
    '''
    管理文章视图 
    '''
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination=pagination, posts=posts)


@admin_bp.route('/settings')
def settings():
    return render_template('admin/settings.html')