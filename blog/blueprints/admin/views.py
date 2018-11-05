from flask import render_template

from flask_login import login_required

from . import admin_bp


@admin_bp.before_request
@login_required
def login_protect():
    '''
    为 admin 蓝本下的所有视图函数添加保护
    '''
    pass


@admin_bp.route('/settings')
def settings():
    return render_template('admin/settings.html')