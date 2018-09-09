# 此文件定义装饰器相关

from functools import wraps
from flask import redirect,url_for,session

# 登录限制装饰器
# 如果已经登录，继续执行函数本身
# 如果未登录，重定向到登录页面
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper