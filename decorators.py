from functools import wraps
from flask import g,redirect,url_for

# 定义一个装饰器，用来检查用户是否登录
def login_required(func):
    ## 保留func信息
    @wraps(func)###
    def wrapper(*args,**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return func(*args,**kwargs)
    return wrapper
