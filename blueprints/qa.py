import pymysql
## 导入蓝图
from flask import (Blueprint, g, jsonify, redirect, render_template, request,
                   url_for)
from flask_paginate import Pagination
from sqlalchemy import func, or_
from werkzeug.security import check_password_hash, generate_password_hash

from decorators import login_required
from exts import db
from models import (KnowledgePointModel, Mindmap, QuestionAnswerModel, Records,
                    UserModel, user_knowledge_level)

# from decorators import login_required
# from models import UserModel,Image
# from models import Question,KnowledgePoint,get_search_results  ## 导入问题答案表  导入问题表  导入知识点表
##  连接数据库
DIFFCULTY = {
    '1':['难度1','难度2'],
    '2':['难度3','难度4'],
    '3':['难度5']
}
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
    # print(2)
    # Query the database to get the updated list of questions
    # This is just a placeholder, replace with your actual query
    ### 推荐算法
    #### 1.获取题目未加入限定条件（即获取全部题目 需修改）
    # questionss = db.session.query(QuestionAnswerModel).all()[10:15]
    #### 2.xxxx
    #### 3.xxxx

    # Render the questions to an HTML string using a Jinja2 template
    # You need to create a new template 'questions.html' for this
    ##
    # html_string = render_template('mainpage.html', questions=questions)
    # questions_data = [question.to_dict() for question in questions]
    # Return the HTML string
    ### questions为推荐题目
    # return render_template('mainpage.html', questions=questions)

    # Convert the questions to a list of dictionaries
    # questions = [question.to_dict() for question in questionss]

    ### 根据 scores  konwledge_level type_level题型水平  来获取题目

    ##
    #user_level,knowledge_level = (id,0,0)
    #for all questions
    #
    #
    #
    #
    questionss= db.session.query(QuestionAnswerModel).all()
    



    questions = []
    for question in questionss:
        question_dict = {
            'id': question.id,
            'content': question.content,
            'question_path': question.question_path,
            # 其他属性
        }
    
        questions.append(question_dict)

    # 返回 JSON 格式的数据

    print('-----------------------questions-----------------------')
    print(questions)
    return jsonify(questions=questions)
    #
    # return jsonify(questions=questions)

##################### 存储头像  放到数据库中
@bp.route('/ranking',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def ranking():
    ### 请求？？？？写不写
    ## 按照user_answer_path  或者user_answer_content存在进行计数 然后进行排序得到user_rank

    user_rank = db.session.query(
        UserModel.id,
        UserModel.name,
        func.count().label('count')
    ).join(
        Records, UserModel.id == Records.user_id
    ).filter(
        or_(Records.user_answer_path != '', Records.user_answer_content != '')
    ).group_by(
        UserModel.id,
        UserModel.name
    ).order_by(
        func.count().desc()
    ).all()
    # user_rank = db.session.query(
    #     Records.user_id,
    #     func.count().label('count')
    # ).filter(
    #     or_(Records.user_answer_path != '', Records.user_answer_content != '')
    # ).group_by(Records.user_id).order_by(func.count().desc()).all()
    print(user_rank)
    # print('user_rank',user_rank[0].count)
    current_user_rank = 0
    for i in range(len(user_rank)):
        if user_rank[i].id==g.user.id:
            current_user_rank = i+1
    print(user_rank)

    # 为了获取我的排名
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
    # diffculty = request.args.get('diffculty')
    # print('----------diffculty----------')
    # print(diffculty)
    # if diffculty == 1:
    #     diffculty = DIFFCULTY[str(diffculty)]
    #     print(diffculty)


    return render_template('challenges.html')
## Challenges
@bp.route('/Challenges',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def Challenges():

    return render_template('Challenges.html')

@bp.route('/tips',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def tips():
    diffculty = request.args.get('diffculty')
    print('-----------------------diffculty-----------------------')
    print(diffculty)


    return render_template('tips.html',diffculty = diffculty)



@bp.route('/challenge',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
@login_required
### 写一个排行榜单页面的后端逻辑代码
def challenge():
    diffculty = request.args.get('diffculty')
    print('----------diffculty----------')
    print(diffculty)
    print(type(diffculty))
    diffculties = DIFFCULTY[diffculty]
    test_questions = db.session.query(QuestionAnswerModel).filter(QuestionAnswerModel.difficulty.in_(diffculties)).limit(10).all()
    print('test_questions',test_questions)
    for name in test_questions:
        print(name)
    print(diffculties)

    return render_template('challenge.html',test_questions = test_questions,diffculty = diffculty)
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
        # 如果Records没有记录这个题目  就增加Records一行数据与 包含question_answer_id 和user_id
        # record = Records.query.filter_by(Records.question_answer_id==id, Records.user_id == g.user.id).first()  filter_by() takes 1 positional argument but 3 were given
        record = Records.query.filter(Records.question_answer_id == id, Records.user_id == g.user.id).first()

        if not record:
            # 如果没有记录这个题目，就增加一行数据到 Records 表中
            # new_record = Records(Records.question_answer_id==id, Records.user_id==g.user.id)  # 假设 g.user 包含了当前用户的信息
            new_record = Records(question_answer_id=id, user_id=g.user.id)

            db.session.add(new_record)
            db.session.commit()
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

        questions_infos = db.session.query(QuestionAnswerModel).filter(QuestionAnswerModel.id == question_answer_id).all()
        # print('questions_infos[0]',questions_infos[0])
        question_path = questions_infos[0].question_path
        answer_path = questions_infos[0].answer_path
        print('question_path', question_path)
        print('answer_path', answer_path)
        scores = db.session.query(Records.scores).filter(Records.question_answer_id == question_answer_id,Records.user_id == g.user.id).all()[0][0]
        # scores = db.session.query(Records.scores).filter(Records.question_answer_id == question_answer_id,Records.user_id == g.user.id).all()[0][0]

        # model为类字典对象

        print('scores',scores)
        return render_template('titlescore.html',question_path = question_path,answer_path = answer_path,question_answer_id = question_answer_id,scores = scores)
    else:
        print('-----------------------修改分数-----------------------')
        data = request.form
        scores = data.get('score')
        questionId = data.get('questionId')
        print('scores',scores)
        print('questionId',questionId)

            # 查看题目类型  并计算得分   查看知识点类型  并计算知识点得分 查看用户能力值  并计算用户得分
        questioninfo = db.session.query(QuestionAnswerModel).filter(QuestionAnswerModel.id == questionId).all()
        question_type = questioninfo[0].question_type
        knowledge_point = questioninfo[0].knowledge_point
        question_difficulty = questioninfo[0].difficulty
        print('question_type',question_type,'knowledge_point',knowledge_point,'question_difficulty',question_difficulty)

        userInfo = db.session.query(UserModel).filter(UserModel.id == g.user.id).all()
        knowledge_point_level = db.session.query(user_knowledge_level).filter(user_knowledge_level.user_id == g.user.id)



        userlevel = userInfo[0].score
        if int(scores)<100:
            #对应题型水平↓
            # type_level
            type_bias = 1
            if question_type == '选择题':
                userInfo[0].Multiple_choice_level = userInfo[0].Multiple_choice_level - type_bias
            elif question_type == '填空题':
                userInfo[0].Fill_blanks_level = userInfo[0].Fill_in_the_blank_level - type_bias
            elif  question_type == '解答题':
                userInfo[0].Short_answer_level = userInfo[0].Short_answer_level - type_bias
            else:
                pass
            #对应知识点水平减少
            for  knowledge in  knowledge_point_level:
                if knowledge[0].knowledge_point_id == knowledge_point:
                    knowledge[0].knowlege_point_level =knowledge[0].knowledge_point_level-type_bias
                
            #用户能力值↓
            #0-20分段特殊处理
            if userInfo[0].score <=20:
                if userInfo[0].score -1<0:#小于0分不再减少
                    userInfo[0].score = 0
                else:
                    userInfo[0].score = userInfo[0].score - 1
            else:#大于0分，按减分公式减少
                userInfo[0].score = userInfo[0].score - (userlevel/(question_difficulty*20))


        elif int(scores) == 100:
            type_bias = 1
            #对应题型水平增加
            if question_type == '选择题':
                userInfo[0].Multiple_choice_level = userInfo[0].Multiple_choice_level + type_bias
            elif question_type == '填空题':
                userInfo[0].Fill_blanks_level = userInfo[0].Fill_in_the_blank_level + type_bias
            elif  question_type == '解答题':
                userInfo[0].Short_answer_level = userInfo[0].Short_answer_level + type_bias
            else:
                pass

            #对应知识点水平增加
            for  knowledge in  knowledge_point_level:
                if knowledge[0].knowledge_point_id == knowledge_point:
                    knowledge[0].knowlege_point_level =knowledge[0].knowledge_point_level+type_bias

            #用户能力水平↑
                    #0-20分段做特殊处理
            if userInfo[0].score <=20: 
                userInfo[0].score = userInfo[0].score +1+question_difficulty
                #20-100分段公式计算
            else:
                if userInfo[0].score+20*question_difficulty/userlevel>100:#大于100分不再增加
                    userInfo[0].score =100
                else:#小于100分按照给分公式增加能力值
                    userInfo[0].score = userInfo[0].score + 20*question_difficulty/userlevel
            #
            db.session.query(UserModel).filter(
                UserModel.id == g.user.id,
                Records.question_answer_id == questionId
                
            ).update({
                UserModel.Multiple_choice_level:userInfo[0].Multiple_choice_level,
                UserModel.Fill_blanks_level:userInfo[0].Fill_blanks_level,
                UserModel.Short_answer_level:userInfo[0].Short_answer_level,
                UserModel.score:userInfo[0].score,

            })

            db.session.query(user_knowledge_level).filter(
                user_knowledge_level.user_id ==g.user.id,
                user_knowledge_level.knowledge_point_id == question_type
            ).update({
                user_knowledge_level.knowledge_point_level:knowledge[0].knowledge_point_level
            })
            db.session.commit()
            ## konwledge_point_level
            ### 处理知识点
            pass
            ## scores level
            pass









        db.session.query(Records).filter(Records.question_answer_id == questionId,Records.user_id == g.user.id).update({Records.scores:scores})
        db.session.commit()

        return jsonify({'code': 200, 'message': '打分成功！','questionId':questionId})

# 添加错题
@bp.route('/add_to_wrong_questions',methods = ['GET','POST'])
@login_required
def add_to_wrong_questions():
    if request.method == 'POST':
        data = request.form
        question_answer_id = data.get('question_answer_id')
        print('-----------------------question_answer_id-----------------------')
        print(question_answer_id)
        # Check if the question is already in wrong questions  0为未加入错题  1为加入错题
        # db.session.query(Records).filter(Records.question_answer_id == question_answer_id,Records.user_id == g.user.id).update({Records.wrong_question:1})
        # 进行错题判断的更新
        wrong_question = db.session.query(Records.wrong_question).filter(Records.question_answer_id == question_answer_id,Records.user_id == g.user.id)[0][0]
        print('-----------------------wrong_question-----------------------')
        print(wrong_question)
        if wrong_question == 1:
            return jsonify({'code': 200, 'message': '请勿重复添加错题！'})
        else:
            db.session.query(Records).filter(Records.question_answer_id == question_answer_id,Records.user_id == g.user.id).update({Records.wrong_question:1})
            db.session.commit()
            return jsonify({'code': 200, 'message': '成功加入错题本！'})


# 移除错题

@bp.route('/remove_from_wrong_questions',methods = ['GET','POST'])
@login_required
def remove_from_wrong_questions():
    if request.method == 'POST':
        ### 获取json数据
        data = request.json
        # 从数据中获取question_answer_id
        question_answer_id = data.get('id')

        # 移除错题
        db.session.query(Records).filter(Records.question_answer_id == question_answer_id,Records.user_id == g.user.id).update({Records.wrong_question:0})
        db.session.commit()
        return jsonify({'code': 200, 'message': '成功移除错题！'})

        # existing_record = Records.query.filter_by(user_id=g.user.id, question_answer_id=question_answer_id).first()
        #
        # if existing_record:
        #     existing_record.favorite = 0
        #     db.session.commit()
        #     print(f'-----------------------题目{question_answer_id}取消收藏成功！-----------------------')
        #     return jsonify({'code': 200, 'message': '取消收藏成功'})
        # else:
        #     print(f'-----------------------题目{question_answer_id}还未收藏！-----------------------')
        #     return jsonify({'code': 400, 'message': '请您先收藏该题目！'})

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


# 保存答案

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
        records = db.session.query(Records).filter(Records.favorite == 1,Records.user_id ==g.user.id).all()
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
        question_answer_id_tuple = db.session.query(Records.question_answer_id).filter(Records.wrong_question==1,Records.user_id == g.user.id).all()
        question_answer_ids = [question_answer_id[0] for question_answer_id in question_answer_id_tuple]
        print('question_answer_ids',question_answer_ids)
        questions = db.session.query(QuestionAnswerModel).filter(QuestionAnswerModel.id.in_(question_answer_ids)).all()
        print('-----------------------questions-----------------------')
        print(type(questions))
        print(questions)

        return render_template('Wrongtitlebook.html',questions = questions)

        ##  为了保持代码复用  不用这种方式
        # pathsTocontents = {}
        # for question_answer_id in question_answer_ids:
        #     # print('question_answer_id',question_answer_id[0])
        #     questions_infos = db.session.query(QuestionAnswerModel.question_path,QuestionAnswerModel.content).filter(QuestionAnswerModel.id == question_answer_id[0]).all()
        #     # print('questions_infos',questions_infos)
        #     pathsTocontents[questions_infos[0][0]] = questions_infos[0][1]
        # print('pathsTocontents',pathsTocontents)
        # return render_template('Wrongtitlebook.html',pathsTocontents = pathsTocontents)
        return jsonify({'code': 400, 'message': '请求方式错误'})

## 错题详情页面
@bp.route('/wrongtitleview',methods = ['GET','POST'])
@login_required
def wrongtitleview():
    questionId = request.args.get('id')
    if request.method == 'GET':
        print('-----------------------GET进来了-----------------------')
        user_answer_infos = db.session.query(Records).filter(Records.question_answer_id == questionId,Records.user_id == g.user.id).all()

        user_answer_path = user_answer_infos[0].user_answer_path
        user_answer_content = user_answer_infos[0].user_answer_content
        scores = user_answer_infos[0].scores
        print('user_answer_path',user_answer_path)
        # 获取题目content和题目img
        questionsinfo = db.session.query(QuestionAnswerModel.answer_path).filter(QuestionAnswerModel.id == questionId).first()[0]

        print(questionsinfo)
        # model为类字典对象

        # return render_template('wrongtitleview.html',question_path = question_path,answer_path = answer_path,questionId = questionId,scores = scores)
        return render_template('wrongtitleview.html',questionsinfo = questionsinfo,user_answer_path = user_answer_path,user_answer_content = user_answer_content,scores = scores,questionId = questionId)


@bp.route('/mindmap_image',methods = ['GET','POST'])
@login_required
def mindmap_image():
    # if request.method == 'GET':
    print('-----------------------GET进来了-----------------------')
    subject_type = request.args.get('map1Value')
    subject_name = request.args.get('map2Value')

    mindmap_info = db.session.query(Mindmap).filter(
        Mindmap.subject_type == subject_type,
        Mindmap.subject_name == subject_name
    ).first()
    if mindmap_info:
        image_url = mindmap_info.mindmap_path  # 假设是图片URL的字段
    else:
        # 如果没有找到对应的Mindmap，使用默认图片
        image_url = '../static/mindmap/数一概率论.png'
    # mindmap_infos = db.session.query(Mindmap).filter(Mindmap.subject_type == subject_type,Mindmap.subject_name == subject_name).all()
    return jsonify({'imageUrl': image_url})
@bp.route('/knowledgeview',methods = ['GET','POST'])
@login_required
def knowledgeview():
    knowledge_point_name = request.args.get('knowledge_point')
    print('knowledge_point_name',knowledge_point_name)

    konwledge_infos = db.session.query(KnowledgePointModel).filter(KnowledgePointModel.knowledge_point_name == knowledge_point_name).all()
    print('konwledge_infos',konwledge_infos)
    return render_template('knowledgeview.html')