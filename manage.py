from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
# 可以用来指定session的保存位置
from flask_session import Session





# 使用类对象创建配置类
class Config():
    DEBUG = True

    SECRET_KEY = "tJrg2EE/sIdQVD8yZmrnCNEgOpYhItcbsNAlGO7MFyXJ+E70ewLsE+yTeLEjDl11ctxEHxXteRDM1GU2YM+AOw=="
    # 为Mysql添加配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/info8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 为redis添加配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # session保存配置
    SESSION_TYPE = "redis"
    # 是否开启session签名
    SESSION_USE_SIGNER = True
    # 指定Session保存的redis
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 设置需要过期
    SESSION_PERMANENT = False
    # 设置过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2





app = Flask(__name__)

# 加载配置
app.config.from_object(Config)
# 初始化数据库
db = SQLAlchemy(app)
# 初始化redis对象
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# 开启当前项目CSRF保护
CSRFProtect(app)



@app.route('/')
def index():
    session["name"] = "INFO8"
    return 'info8'


if __name__ == '__main__':
    app.run(debug=True)

