import datetime
import functools

from manage import app


# def user_login_data(f):
#     @functools.wraps(f)  # 作用:使user_login_data装饰器不会同化名字
#     def wrapper(*args, **kwargs):
#         return f(*args, **kwargs)
#
#     return wrapper
#
#
# @app.route('/news/<int:news_id>')
# @user_login_data
# def num1():
#     print("aaa")
#
#
# # @app.route('/')
# @user_login_data
# def num2():
#     print("bbbb")
#
# if __name__ == '__main__':
#     print(num1.__name__)
#     print(num2.__name__)
import random

from info import db
from info.models import User
from manage import app


def add_test_users():
    users = []
    now = datetime.datetime.now()
    for num in range(30000, 50890):
        try:
            user = User()
            user.nick_name = "%011d" % num
            user.mobile = "%011d" % num
            user.password_hash = "pbkdf2:sha256:50000$SgZPAbEj$a253b9220b7a916e03bf27119d401c48ff4a1c81d7e00644e0aaf6f3a8c55829"
            user.last_login = now - datetime.timedelta(seconds=random.randint(267840 * 3 ,267840 *8))
            users.append(user)
            print(user.mobile)
        except Exception as e:
            print(e)
    # 手动开启一个app的上下文
    with app.app_context():
        db.session.add_all(users)
        db.session.commit()
    print('OK')


if __name__ == '__main__':
    add_test_users()