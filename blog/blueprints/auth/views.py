from flask import (
    render_template,
    flash,
    redirect,
    url_for,
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from . import auth_bp
from ...models import Admin
from ...forms import LoginForm
from ...utils import redirect_back


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            # 验证 username 和 password
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('登录成功', 'info')
                return redirect_back()
            else:
                flash('用户名或密码错误', 'warning')
        else:
            flash('数据库中没有找到管理员信息', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录', 'info')
    return redirect_back()