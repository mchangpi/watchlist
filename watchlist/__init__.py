import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
print('__name__: ' + __name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print('app.root_path: ' + app.root_path)
print('os.path.dirname(app.root_path): ' + os.path.dirname(app.root_path))

db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
login_manager = LoginManager(app)

# 如用户已登录，current_user变量的值会是当前用户的用户模型类记录
@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

# 如果未登录的用户，把用户重定向到登录页面，并显示一个错误提示。
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in first'

# 返回的变量将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用
@app.context_processor
def inject_user():  # 函数名可以随意修改
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}

from watchlist import views, errors, commands