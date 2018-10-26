# 首页的逻辑,包括首页的展示和标题小图标的展示
from flask import Blueprint

# 创建蓝图对象


news_blu = Blueprint("news", __name__, url_prefix='/news')

from . import views