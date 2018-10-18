
from flask import render_template, request, current_app, flash, redirect, url_for

from . import blog_bp
from ...models import Category, Post, Comment
from ...forms import CommentForm
from ...extensions import db
from ...email import send_new_comment_email


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/about')
def about():
    '''
    博客介绍 
    '''
    return render_template('blog/about.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    '''
    分类页面 
    '''
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    '''
    文章详情页面 
    '''
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(
        Comment.timestamp.desc()).paginate(page, per_page)
    comments = pagination.items

    form = CommentForm()
    from_admin = False
    reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        body = form.body.data
        comment = Comment(
            author=author,
            email=email,
            body=body,
            from_admin=from_admin,
            post=post,
            reviewed=reviewed,
        )
        db.session.add(comment)
        db.session.commit()
        flash('您的评论将在审核通过后显示', 'info')
        print('start send')
        send_new_comment_email(post) # 发送提醒邮件给博主
        return redirect(url_for('blog.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)