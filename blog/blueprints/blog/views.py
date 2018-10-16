
from flask import render_template

from . import blog_bp
from ...models import Category


@blog_bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('blog/index.html', categories=categories)