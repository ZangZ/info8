# 新闻详情模块的蓝图

from flask import Blueprint, session, request, url_for, redirect

# 创建蓝图对象
admin_blu = Blueprint("admin", __name__)


from . import views




@admin_blu.before_request
def check_admin():
    # 如果不是管理员没那么直接跳转到主页
    is_admin = session.get("is_admin", False)
    # if not is_admin and 当前访问的url不是管理员登录页
    if not is_admin and not request.url.endswith(url_for('admin.login')):
        return redirect('/')