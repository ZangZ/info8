from logging.handlers import RotatingFileHandler
from urllib import response

from flask import Flask, logging
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from redis import StrictRedis
from config import config
import logging


# 初始化数据库
from info.utils.common import do_index_class

db = SQLAlchemy()

redis_store = None # type: StrictRedis


def setup_log(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):  # create_app就类似于工厂方法
    # 配置日志
    setup_log(config_name)
    # 创建flask对象
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])

    # 通过app初始化
    db.init_app(app)
    # 初始化 redis 存储对象
    global redis_store
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT,decode_responses=True)
    # 开启当前项目 CSRF 保护，只做服务器验证功能
    CSRFProtect(app)
    # 设置session保存指定位置
    # 帮我们做了:从cookie中取出随机值,从表单中取出随机值,然后进行校验,并且响应校验结果
    # 我们需要做:1.在界面加载的时候,往cookie中添加一个csrf_token,并且在表单中添加一个隐藏的csrf_token
    # 在响应里设置cookie,很多地方都需要设置cookie,使用钩子函数:after_response
    # 我们现在登录或注册不是使用表单,而是使用ajax,所以需要在ajax请求的时候带上csrf_token
    Session(app)

    # 添加自定一过滤器
    # app.add_template_filter(do_index_class, "index_class")
    app.add_template_filter(do_index_class, "index_class")


    @app.after_request
    def after_resquest(response):
        csrf_token = generate_csrf()  # 生成随机的csrf_token值
        # 设置一个cookie
        response.set_cookie("csrf_token", csrf_token)
        return response



    # 注册蓝图
    # 注册蓝图时,什么时候注册,什么时候导入
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    from info.modules.news import news_blu
    app.register_blueprint(news_blu)

    return app