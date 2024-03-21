from flask import render_template,request,url_for,redirect
from flask import g
from flask import jsonify
from flask_paginate import Pagination
## 导入蓝图
from flask import Blueprint
from flask import g
from decorators import login_required
from werkzeug.security import generate_password_hash,check_password_hash
from exts import db
from models import UserModel,QuestionAnswerModel,Records
import pymysql
# from decorators import login_required
# from models import UserModel,Image
# from models import Question,KnowledgePoint,get_search_results  ## 导入问题答案表  导入问题表  导入知识点表
##  连接数据库

bp = Blueprint('qa',__name__,url_prefix='/')


##################### mainpage页面
@bp.route('/',methods = ['GET','POST'])
def index():
    print(1)
    if request.method == 'GET':
        ### 从question_answer表中获取所有数据
        questions = db.session.query(QuestionAnswerModel).all()
        ### 创建分页 第一个page必选项  page从agrs来，如果没有默认值为1
        page = request.args.get('page',1,type=int)
        ### Query the database and paginate the results
        # questions = QuestionAnswerModel.query.paginate(page,per_page=10)
        # questions = QuestionAnswerModel.query.paginate(page=page, per_page=10, error_out=False)
        questions = QuestionAnswerModel.query.paginate(page=page, per_page=3, error_out=False)
        return render_template('mainpage.html',questions = questions)

        ### 如果只想获取某列的话
        # db.session.query(QuestionAnswerModel).filter(QuestionAnswerModel.id>10).all()



        # return render_template('mainpage.html',questions)

    return render_template('mainpage.html')

### 更新题目
@bp.route('/get_updated_questions', methods=['GET'])
def get_updated_questions():
    print(2)
    # Query the database to get the updated list of questions
    # This is just a placeholder, replace with your actual query
    ### 推荐算法
    #### 1.获取题目未加入限定条件（即获取全部题目 需修改）
    questions = db.session.query(QuestionAnswerModel).all()
    #### 2.xxxx
    #### 3.xxxx

    # Render the questions to an HTML string using a Jinja2 template
    # You need to create a new template 'questions.html' for this
    ##
    # html_string = render_template('mainpage.html', questions=questions)
    # questions_data = [question.to_dict() for question in questions]
    # Return the HTML string
    ### questions为推荐题目
    return render_template('mainpage.html', questions=questions)

##################### 存储头像  放到数据库中
@bp.route('/ranking',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def ranking():
    ### 请求？？？？写不写
    # # 查询用户排行榜数据，按得分降序排列
    user_rank = db.session.query(UserModel).order_by(UserModel.score.desc()).all()
    # 为了获取我的排名
    current_user_rank = user_rank.index(g.user)+1
    # 总人数
    total_user = len(user_rank)
    # 我的排名/总人数
    # myrank = {'current_user_rank':current_user_rank,'user':g.user}
    myrank = {'current_user_rank':current_user_rank,'total_user':total_user}

    # scores = db.session.query(UserModel).order_by(UserModel.score.desc()).all()
    # scores = db.session.query(UserModel).order_by(UserModel.scores.desc()).all()
    # ### scores  为所有的行对象

    # return render_template('leaderboard.html', scores=scores)
    return render_template('ranking.html', user_rank = user_rank,myrank = myrank)


@bp.route('/mindmap',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def mindmap():
    # # 查询用户排行榜数据，按得分降序排列
    # scores = db.session.query(UserModel).order_by(UserModel.scores.desc()).all()
    # ### scores  为所有的行对象

    # return render_template('leaderboard.html', scores=scores)
    return render_template('mindmap.html')
@bp.route('/practicecheck',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def practicecheck():
    # # 查询用户排行榜数据，按得分降序排列
    # users_rank = db.session.query(UserModel).order_by(UserModel.scores.desc()).all()
    # scores = db.session.query(UserModel).order_by(UserModel.scores.desc()).all()
    # ### scores  为所有的行对象

    # return render_template('leaderboard.html', scores=scores)
    return render_template('practicecheck.html')
    # return render_template('practicecheck.html', users_rank=users_rank)

@bp.route('/challenges',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def challenges():

    return render_template('challenges.html')

#########################titleview
@bp.route('/titleview',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def titleview():
    id = request.args.get('id')
    print('-----------------------id-----------------------')
    print(id)
    # 查询数据库获取题目信息
    question = QuestionAnswerModel.query.get(id)
    if question:
        # 如果找到了题目，将题目信息传递给模板进行渲染
        return render_template('titleview.html', question=question)
    else:
        # 如果未找到题目，可以返回一个错误页面或者重定向到其他页面
        return render_template('error.html', message='题目不存在')
    # if request.method=='GET':
    #     data = request.get_json()
    #
    #     # 从数据中获取imageId
    #     question_answer_id = data.get('id')
    #     # 从数据库中获取question_answer_object对象
    #     question_answer_object = QuestionAnswerModel.query.get(question_answer_id)

    #
    #
    # return render_template('titleview.html')



### titlescores页面显示
@bp.route('/titlescore',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
def titlescore():
    if request.method == 'GET':
        print('-----------------------GET进来了-----------------------')
        question_answer_id = request.args.get('question_id')
        print(f'-----------------------question_answer_id为{question_answer_id}-----------------------')
        # user_answer_content = db.session.query(Records.user_answer_content).filter(Records.question_answer_id == question_answer_id,Records.user_id == g.user.id).all()[0][0]
        # user_answer_path = db.session.query(Records.user_answer_path).filter(Records.question_answer_id == question_answer_id,Records.user_id == g.user.id).all()[0][0]
        # print('user_answer_content',user_answer_content)#user_answer_content [('跳转',)]
        # print('user_answer_path',user_answer_path)#user_answer_path [('uploads\\Snipaste_2024-03-09_17-58-37.png',)]
        questions_infos = db.session.query(QuestionAnswerModel).filter(QuestionAnswerModel.id == question_answer_id).all()
        # print('questions_infos[0]',questions_infos[0])
        question_path = questions_infos[0].question_path
        answer_path = questions_infos[0].answer_path
        # model为类字典对象
        print('question_path',question_path)
        print('answer_path',answer_path)
        return render_template('titlescore.html',question_path = question_path,answer_path = answer_path,question_answer_id = question_answer_id)
    else:
        print('-----------------------修改分数-----------------------')
        data = request.form
        scores = data.get('score')
        questionId = data.get('questionId')
        db.session.query(Records).filter(Records.question_answer_id == questionId,Records.user_id == g.user.id).update(scores = scores)
        db.session.commit()
        return render_template('titlescore.html')

@bp.route('/add_to_favorites',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def add_to_favorites():
    if request.method == 'POST':
        ### 获取json数据
        data = request.json
        # 从数据中获取question_answer_id
        question_answer_id = data.get('id')

        # Check if the question is already in favorites
        existing_record = Records.query.filter_by(user_id=g.user.id, question_answer_id=question_answer_id).first()
        if existing_record:
            print(f'-----------------------题目{question_answer_id}收藏成功-----------------------')
            return jsonify({'code': 200, 'message': '题目已在收藏夹中'})

        ### 把收藏存储到record表中
        record = Records()
        record.question_answer_id = question_answer_id
        record.user_id = g.user.id
        record.favorite = 1
        ### 存入records表
        db.session.add(record)
        db.session.commit()


        # # 从数据库中获取question_answer_object对象
        # question_answer_object = QuestionAnswerModel.query.get(question_answer_id)
        # 将题目加入到收藏夹
        # g.user.favorites.append(question_answer_id)
        # db.session.commit()
        print(f'-----------------------题目{question_answer_id}收藏成功-----------------------')
        return jsonify({'code': 200, 'message': '收藏成功'})
    else:
        return jsonify({'code': 400, 'message': '请求方式错误'})
### 取消收藏
# cancel_to_favorites
@bp.route('/cancel_to_favorites',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def cancel_to_favorites():
    if request.method == 'POST':
        ### 获取json数据
        data = request.json
        # 从数据中获取question_answer_id
        question_answer_id = data.get('id')

        # Check if the question is already in favorites
        existing_record = Records.query.filter_by(user_id=g.user.id, question_answer_id=question_answer_id).first()

        if existing_record:
            existing_record.favorite = 0
            db.session.commit()
            print(f'-----------------------题目{question_answer_id}取消收藏成功！-----------------------')
            return jsonify({'code': 200, 'message': '取消收藏成功'})
        else:
            print(f'-----------------------题目{question_answer_id}还未收藏！-----------------------')
            return jsonify({'code': 400, 'message': '请您先收藏该题目！'})


        # ### 把收藏存储到record表中
        # record = Records()
        # record.question_answer_id = question_answer_id
        # record.user_id = g.user.id
        # record.favorite = 1
        # ### 存入records表
        # db.session.add(record)
        # db.session.commit()


        # # 从数据库中获取question_answer_object对象
        # question_answer_object = QuestionAnswerModel.query.get(question_answer_id)
        # 将题目加入到收藏夹
        # g.user.favorites.append(question_answer_id)
        # db.session.commit()
        print(f'-----------------------题目{question_answer_id}收藏成功-----------------------')
        return jsonify({'code': 200, 'message': '收藏成功'})
    else:
        return jsonify({'code': 400, 'message': '请求方式错误'})

# 个人信息视图及其函数
@bp.route('/personalinformation',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def personalinformation():
    if request.method == 'GET':
        print('-----------------------GET进来了-----------------------')
        return render_template('personalinformation.html')
    else:
        print('-----------------------POST进来了-----------------------')
        ### 获取表单数据
        data = request.form
        name = data.get('nickname')
        password = data.get('password')
        school = data.get('school')
        major = data.get('major')
        email = data.get('email')
        user = UserModel()
        ## 判断有没有这个email  flask 修改  是要找到实体  然后对实体进行属性的的修改
        # 使用tutorial
        # shown in the
        # Flask - SQLAlchemy
        # documentation检索对象。一旦您有了要更改的实体，请更改实体本身。然后是db.session.commit()。
        existing_user = UserModel.query.filter_by(email=email).first()
        if existing_user:
            existing_user.name = name
            existing_user.password = password
            existing_user.school = school
            existing_user.major = major
            existing_user.email = email
            db.session.commit()

            # 再添加
            # user.name = name
            # user.password = password
            # user.school = school
            # user.major = major
            # user.email = email
            # db.session.add(user)
            # db.session.commit()
            # # 先删除这条数据
            # db.session.delete(existing_user)
            # db.session.commit()

        else:
            user.name = name
            user.password = password
            user.school = school
            user.major = major
            user.email = email
            db.session.add(user)
            db.session.commit()
        # db.session.merge(user)

        print('-----------------------数据库更新成功-----------------------')
        return redirect(url_for('qa.personalinformation'))
        ## 更新数据库
        # user.name = name
        # user.password = password
        # user.school = school
        # user.major = major
        # user.email = email
        # ###
        # db.session.add(user)
        # db.session.commit()
        # return redirect(url_for('qa.personalinformation'))


        #
        # # 连接数据库
        # conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='mathproblcu')
        # # 获取游标
        # cursor = conn.cursor()
        # # 执行查询
        # cursor.execute('SELECT * FROM users')
        #
        # # 获取查询结果
        # results = cursor.fetchall()
        #
        # existing_user = UserModel.query.filter_by(email=email).first()
        # if existing_user:
        #     # 执行查询
        #     cursor.execute("UPDATE user SET name=name, password=password, school=school, major=major WHERE email=email")
        #
        #     # 获取查询结果
        #     results = cursor.fetchall()
        #     print(results,'results')

        #     ## 存入数据库
        #     user = UserModel()
        #     user.name = name
        #
        # # 注释掉  加密
        # # user.password = generate_password_hash(password)
        #     user.password = password
        #     # user.email = email
        #     user.school = school
        #     user.major = major
        #     print('user.name', user.name)
        #     print('user.password', password)
        #     print('user.school', school)
        #     print('user.major', user.major)
        # # 更新数据库
        # # db.session.update(user)
        # #     db.session.commit()
        # else:
        #     new_user = UserModel(name=nickname, password=password, email=email, school=school, major=major)
        #     db.session.add(new_user)
        #     # db.session.commit()
        # try:
        #     db.session.commit()
        #     print('-----------------------数据库更新成功-----------------------')
        # except Exception as e:
        #     print(e)
        #     db.session.rollback()
        #     print('-----------------------数据库更新失败-----------------------')
        ### 返回qa.personlinformation页面  就是GET方法  就会直接render_template('personalinformation.html')
        # return redirect(url_for('qa.personalinformation'))



    # if request.method == 'POST':
    #     ### 获取json数据
    #     data = request.json
    #     # 从数据中获取question_answer_id
    #     question_answer_id = data.get('id')
    #
    #     # Check if the question is already in favorites
    #     existing_record = Records.query.filter_by(user_id=g.user.id, question_answer_id=question_answer_id).first()
    #     if existing_record:
    #         print(f'-----------------------题目{question_answer_id}收藏成功-----------------------')
    #         return jsonify({'code': 200, 'message': '题目已在收藏夹中'})
    #
    #     ### 把收藏存储到record表中
    #     record = Records()
    #     record.question_answer_id = question_answer_id
    #     record.user_id = g.user.id
    #     record.favorite = 1
    #     ### 存入records表
    #     db.session.add(record)
    #     db.session.commit()


        # # 从数据库中获取question_answer_object对象
        # question_answer_object = QuestionAnswerModel.query.get(question_answer_id)
        # 将题目加入到收藏夹
        # g.user.favorites.append(question_answer_id)
        # db.session.commit()
    #     print(f'-----------------------题目{question_answer_id}收藏成功-----------------------')
    #     return jsonify({'code': 200, 'message': '收藏成功'})
    # else:
    #     return jsonify({'code': 400, 'message': '请求方式错误'})

### 收藏夹视图及其函数
@bp.route('/collection',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def collection():
    ### 取消收藏的POST放给另一个路由cancel_to_favorites去做了
    if request.method == 'GET':
        ### 从record表中获取收藏的数据
        records = db.session.query(Records).filter(Records.favorite == 1).all()
        question_answer_ids = [record.question_answer_id for record in records]
        print('-----------------------question_answer_ids-----------------------')
        print(question_answer_ids)

        ### .in_ 必须要列表
        questions = db.session.query(QuestionAnswerModel).filter(QuestionAnswerModel.id.in_(question_answer_ids)).all()
        print('-----------------------questions-----------------------')
        print(type(questions))
        print(questions)

    # ### 创建分页 第一个page必选项  page从agrs来x，如果没有默认值为1
    #     page = request.args.get('page',1,type=int)
    #     ### Query the database and paginate the results
    #     # questions = QuestionAnswerModel.query.paginate(page,per_page=10)
    #     # questions = QuestionAnswerModel.query.paginate(page=page, per_page=10, error_out=False)
    #     questions = QuestionAnswerModel.query.paginate(page=page, per_page=3, error_out=False)
        return render_template('collection.html',questions = questions)




        ## 通过backref  获取


        ### 如果只想获取某列的话
        # db.session.query(QuestionAnswerModel).filter(QuestionAnswerModel.id>10).all()
    # if request.method == 'POST':
    #     ### 获取json数据
    #     data = request.json
    #     # 从数据中获取question_answer_id
    #     question_answer_id = data.get('id')
    #
    #     # Check if the question is already in favorites
    #     existing_record = Records.query.filter_by(user_id=g.user.id, question_answer_id=question_answer_id).first()
    #     if existing_record:
    #         print(f'-----------------------题目{question_answer_id}收藏成功-----------------------')
    #         return jsonify({'code': 200, 'message': '题目已在收藏夹中'})
    #
    #     ### 把收藏存储到record表中
    #     record = Records()
    #     record.question_answer_id = question_answer_id
    #     record.user_id = g.user.id
    #     record.favorite = 1
    #     ### 存入records表
    #     db.session.add(record)
    #     db.session.commit()
    #
    #
    #     # # 从数据库中获取question_answer_object对象
    #     # question_answer_object = QuestionAnswerModel.query.get(question_answer_id)
    #     # 将题目加入到收藏夹
    #     # g.user.favorites.append(question_answer_id)
    #     # db.session.commit()
    #     print(f'-----------------------题目{question_answer_id}收藏成功-----------------------')
    #     return jsonify({'code': 200, 'message': '收藏成功'})
    # else:
    #     return jsonify({'code': 400, 'message': '请求方式错误'})

### 错题本 视图及其函数
@bp.route('/wrongtitlebook',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def wrongtitlebook():
    if request.method == 'POST':
        ### 获取json数据
        data = request.json
        # 从数据中获取question_answer_id
        question_answer_id = data.get('id')

        # Check if the question is already in favorites
        existing_record = Records.query.filter_by(user_id=g.user.id, question_answer_id=question_answer_id).first()
        if existing_record:
            print(f'-----------------------题目{question_answer_id}收藏成功-----------------------')
            return jsonify({'code': 200, 'message': '题目已在收藏夹中'})

        ### 把收藏存储到record表中
        record = Records()
        record.question_answer_id = question_answer_id
        record.user_id = g.user.id
        record.favorite = 1
        ### 存入records表
        db.session.add(record)
        db.session.commit()


        # # 从数据库中获取question_answer_object对象
        # question_answer_object = QuestionAnswerModel.query.get(question_answer_id)
        # 将题目加入到收藏夹
        # g.user.favorites.append(question_answer_id)
        # db.session.commit()
        print(f'-----------------------题目{question_answer_id}收藏成功-----------------------')
        return jsonify({'code': 200, 'message': '收藏成功'})
    else:
        return jsonify({'code': 400, 'message': '请求方式错误'})



