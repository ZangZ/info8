from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from sqlalchemy.orm import Session





# 使用类对象创建配置类
class Config():
    DEBUG = True
    # 为Mysql添加配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/info8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 为redis添加配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379




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
    return 'info8'


if __name__ == '__main__':
    app.run(debug=True)

