from flask import Blueprint, render_template


blog_bp = Blueprint('blog', __name__)

from . import views