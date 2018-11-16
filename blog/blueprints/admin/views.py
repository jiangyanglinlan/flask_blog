from flask import (
    render_template,
    request,
    current_app,
    redirect,
    url_for,
    flash,
)
from flask_login import login_required

from . import admin_bp
from ...extensions import db
from ...models import Post, Category, Comment
from ...forms import PostForm
from ...utils import redirect_back


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


@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash('发表成功.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('文章更新成功.', 'success')
        return redirect(url_for('blog.show_post', post_id=post_id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('删除文章成功', 'success')
    return redirect_back()


@admin_bp.route('/comment/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('删除评论成功', 'success')
    return redirect_back()


@admin_bp.route('/set-comment/<int:post_id>', methods=['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('当前文章设置为禁止评论', 'info')
    else:
        post.can_comment = True
        flash('当前文章设置为允许评论.', 'info')
    db.session.commit()
    return redirect(url_for('blog.show_post', post_id=post_id))


@admin_bp.route('/settings')
def settings():
    return render_template('admin/settings.html')