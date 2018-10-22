# 首页的逻辑,包括首页的展示和标题小图标的展示
from flask import Blueprint

# 创建蓝图对象


index_blu = Blueprint("index", __name__)

from . import views