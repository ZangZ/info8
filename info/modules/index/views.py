from flask import render_template, current_app

from info import redis_store
from . import index_blu



@index_blu.route("/")
def index():
    return render_template("news/index.html")

# 打开浏览器的时候浏览器会默认请求跟路由路径+ favicon.ico作为网站的小图标
@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")