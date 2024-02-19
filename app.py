from flask import Flask,session,g
from models import *
## 导入数据库
from flask_migrate import Migrate
import config
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from exts import db,mail

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
mail.init_app(app)


migration = Migrate(app,db)

### 注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
### session---》user_id  绑定到对象  再执行视图函数限制性before_request
# 在执行视图函数前
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    # 判断session是否存在、
    if user_id:
        # 如果存在
        # setattr(x, 'y', v) is equivalent to ``x.y = v ''
        # setattr(g, 'user', UserModel.query.get(user_id))
        # 绑定到全局对象
        g.user = UserModel.query.get(user_id)
    else:
        g.user = None

# 上下文处理器  所有模板库可以获得这个对象
@app.context_processor
def my_context_process():
    return {'user':g.user}
### 所有模板都可以使用  user  user的值为g.user


if __name__ == '__main__':
    app.run(debug=True)



