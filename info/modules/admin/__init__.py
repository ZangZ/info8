# 新闻详情模块的蓝图

from flask import Blueprint

# 创建蓝图对象
admin_blu = Blueprint("admin", __name__)


from . import views