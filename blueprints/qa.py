from flask import render_template,request,url_for,redirect
from flask import g
from flask import jsonify
## 导入蓝图
from flask import Blueprint
from flask import g
from decorators import login_required
from werkzeug.security import generate_password_hash,check_password_hash
from exts import db
# from decorators import login_required
# from models import UserModel,Image
# from models import Question,KnowledgePoint,get_search_results  ## 导入问题答案表  导入问题表  导入知识点表
##  连接数据库

bp = Blueprint('qa',__name__,url_prefix='/')



@bp.route('/')
def index():
    return render_template('mainpage.html')

### 存储头像  放到数据库中
@bp.route('/ranking',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def ranking():
    # # 查询用户排行榜数据，按得分降序排列
    # scores = db.session.query(UserModel).order_by(UserModel.scores.desc()).all()
    # ### scores  为所有的行对象

    # return render_template('leaderboard.html', scores=scores)
    return render_template('ranking.html', scores=0)
