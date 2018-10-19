from flask import session
from flask_script import Manager
# 导入数据迁移
from flask_migrate import Migrate, MigrateCommand
from info import app,db


manager = Manager(app)
Migrate(app, db)
# 将迁移命令添加到manager中
manager.add_command("db", MigrateCommand)


@app.route('/')
def index():
    session["name"] = "itheima"
    return 'index8888888'


if __name__ == '__main__':
    manager.run()
