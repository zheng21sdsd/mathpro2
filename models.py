# 建表
from exts import db
from datetime import datetime
class UserModel(db.Model):
    __tablename__ = 'user' #在数据库中建了一张名为user的表，其中表含有id，username，password，email，join_time
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)#primary_key为主键 autoincrement = True 表示自动增加
    name = db.Column(db.String(50),nullable = False)#属性或者列名一般都是（类别，可不可空，default = “”缺省值）
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False,unique = True)
    school = db.Column(db.String(100), nullable=False) # 属性或者列名一般都是（类别，可不可空，default = “”缺省值）
    major = db.Column(db.String(100), nullable=False)  ## 专业

    score = db.Column(db.Integer, default=0)  ## 默认积分为0
    avatar = db.Column(db.String(100), nullable=False) ## 头像路径

    join_time = db.Column(db.DateTime,default=datetime.now)#datatime.now这个表示调用这个函数
                                                         # datatime.now（）是一个值 不是调用函数

    # user_question_num = db.Column(db.Integer, default=0)  # 提问数
class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
class Records(db.Model):
    ''' (
  `records_id` int NOT NULL AUTO_INCREMENT COMMENT '用户刷题记录主键',
  `question_answer_id` int NOT NULL COMMENT '题目id',
  `user_id` int NOT NULL COMMENT '用户id',
  `favorite` int NULL DEFAULT NULL COMMENT '是否收藏该题目，1为收藏，0为未收藏',
  `wrong_question` int NULL DEFAULT NULL COMMENT '是否加入到错题本，1为加入，0为未加入',
  `user_answer_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户自己的答案路径',
  `user_answer_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '如果是选择题直接填写内容，如果非选择题上传图片到user_answer_path字段',
  `record_time` datetime NULL DEFAULT NULL COMMENT '做题时间',
  PRIMARY KEY (`records_id`) USING BTREE,
  INDEX `user_id_records_foreignkey`(`user_id` ASC) '''
    __tablename__ = 'records'
    records_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_answer_id = db.Column(db.Integer,db.ForeignKey('question_answers.id'))

    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))## 作为外键 一对多
    favorite = db.Column(db.Integer, default=0)  # 是否收藏该题目，1为收藏，0为未收藏
    wrong_question = db.Column(db.Integer, default=0)  # 是否加入到错题本，1为加入，0为未加入
    user_answer_path = db.Column(db.String(255), nullable=True)  # 用户自己的答案路径
    user_answer_content = db.Column(db.String(255), nullable=True)  # 如果是选择题直接填写内容，如果非选择题上传图片到user_answer_path字段
    record_time = db.Column(db.DateTime, default=datetime.now)  # 做题时间

    question_answer = db.relationship('QuestionAnswerModel',backref = 'records')
    user = db.relationship('UserModel',backref = 'records')

