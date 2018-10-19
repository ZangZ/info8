from flask import session
from flask_script import Manager
# 导入数据迁移
from flask_migrate import Migrate, MigrateCommand
from info import create_app,db
import logging

app = create_app("development")
manager = Manager(app)
Migrate(app, db)
# 将迁移命令添加到manager中
manager.add_command("db", MigrateCommand)


@app.route('/')
def index():
    session["name"] = "itheima"
    logging.debug("测试debug")
    logging.warning("测试warning")
    logging.error("测试error")
    logging.fatal("测试fatal")

    return 'index898465123'


if __name__ == '__main__':
    manager.run()
