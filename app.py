from flask import Flask,session,g,request,jsonify
from models import *
## 导入数据库
from flask_migrate import Migrate
import config
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from exts import db,mail
import os
from flask import render_template
app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)


migration = Migrate(app,db)

### 注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


### 提交答案 submit_answer

UPLOAD_FOLDER = 'static/uploads_answers'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# @app.route('/submit_answer',methods = ['GET','POST'])
# 每次一个函数都得进行g.user判断  所有我们可以用一个装饰器  来解决这个问题
# @login_required
# def submit_answer():
#     # id = request.args.get('id')
#     # print('-----------------------id-----------------------')
#     # print(id)
#     # # 查询数据库获取题目信息
#     # question = QuestionAnswerModel.query.get(id)
#     # if question:
#     #     # 如果找到了题目，将题目信息传递给模板进行渲染
#     #     return render_template('titleview.html', question=question)
#     # else:
#     #     # 如果未找到题目，可以返回一个错误页面或者重定向到其他页面
#     #     return render_template('error.html', message='题目不存在')
#
#
#
#     if request.method=='GET':
#         data = request.get_json()
#         TextValue = data.get('textValue')
#         print('-----------------------textValue-----------------------')
#         print(TextValue)
#
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file part','code':400})
#             # return redirect(request.url)
#
#         file = request.files['file']
#
#         if file.filename == '':
#             return jsonify({'error': 'No selected file','code':400})
#             # return redirect(request.url)
#
#
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#             ## Save image information to the database
#             ## 判断用户是否有图片  有就更新  没有就添加
#             if Records.query.filter_by(user_id=g.user.id).first().user_answer_content:  ##'default.jpg'
#                 pass
#             else:
#                 # record = Records(user_answer_content=TextValue, user_answer_filepath=filepath, user_id=g.user.id)
#                 record = Records(user_answer_content=TextValue,user_id=g.user.id)
#                 db.session.add(record)
#                 db.session.commit()
#             return jsonify({'message': 'File uploaded successfully', 'filepath': filepath})
#         else:
#             return jsonify({'error': 'File type not allowed'})
@app.route('/submit_answer',methods = ['GET','POST'])
def submit_answer():

    # 确保上传文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    questionId = request.args.get('questionId')
    print('questionId',questionId)
    # 获取文本字段
    text_value = request.form.get('textValue')
    # questionId = request.form.get('questionId')

    # 处理上传的图片文件
    files = request.files
    for file_key in files:
        file = files[file_key]
        if file and file.filename:
            # 保存文件到服务器的上传文件夹
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            print('-----------------------保存图片路径-----------------------')
            print(filepath)
            file.save(filepath)
    # 上传图片路径搭配record数据库中
    # db.session.query(Records).filter(Records.user_id == g.user.id and ).update({Records.user_answer_content: text_value, Records.user_answer_filepath: filepath})
    # flask 联合表查询
    # db.session.query(Records).filter(Records.user_id == g.user.id,Records.question_answer_id == questionId).update({Records.user_answer_content: text_value, Records.user_answer_filepath: filepath})
    # 更新记录
            print('-----------------------更新记录-----------------------')
            print(text_value)
            print('questionId',questionId)
            db.session.query(Records).filter(
                Records.user_id == g.user.id,
                Records.question_answer_id == questionId
            ).update({
                Records.user_answer_content: text_value,
                Records.user_answer_path: filepath
            })

            # 提交更改到数据库
            db.session.commit()
    # 返回一个成功的响应
    # 返回页面  并且带着这些数据
    sendmess = {'code': 200, 'message': '提交成功！'}
    # return render_template('titlescore.html',questionId=questionId,sendmess=sendmess)
    return jsonify(code=200, message="提交成功！")


@app.route('/save_answers',methods = ['GET','POST'])

def save_answers():

    print('-----------------------save_answers-----------------------')
    if request.method == 'POST':
        # 处理表单文本数据
        text_data = request.form.to_dict()  # 包含了问题ID和相应的文本答案

        # 处理文件上传
        files = request.files.to_dict()  # 包含了问题ID和相应的文件对象

        for question_id_text, text_value in text_data.items():
            print(f'问题ID：{question_id_text}，文本答案：{text_value}')
            question_id = question_id_text.split('-')[-1]
            # input('-----------------------input-----------------------' )
            # 对应问题的文件对象
            file = files.get(f'file-{question_id}')  # 假设前端字段名为'file-问题ID'

            filepath = None
            if file and file.filename:
                # 保存文件到服务器的上传文件夹
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                print(f'文件已保存到：{filepath}')

            # 在这里进行数据库更新操作
            # 假设 g.user.id 包含了当前用户的ID，确保你的应用有途径获取当前用户ID
            user_id = g.user.id  # 示例用户ID，根据实际情况获取

            # 查找或创建数据库记录
            record = db.session.query(Records).filter(
                Records.user_id == user_id,
                Records.question_answer_id == question_id
            ).first()

            if not record:
                # 如果没有找到记录，则创建新记录
                record = Records(
                    user_id=user_id,
                    question_answer_id=question_id,
                    user_answer_content=text_value,
                    user_answer_path=filepath
                )
                db.session.add(record)
            else:
                # 如果找到了记录，则更新记录
                record.user_answer_content = text_value
                record.user_answer_path = filepath

            # 提交更改到数据库
            db.session.commit()

        # 返回一个成功的响应
        return jsonify(code=200, message='保存成功！')

    # if request.method=='POST':
    #     text_data = request.form.to_dict()
    #     print("接收到的文本数据:", text_data)
    #     # 处理文件上传
    #     files = request.files.to_dict()
    #     for key,file in files.items():
    #         if file and file.filename:
    #             # 保存文件到服务器的上传文件夹
    #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    #             print('-----------------------保存图片路径-----------------------')
    #             print(filepath)
    #             file.save(filepath)
    #             # flask 联合表查询
    #             # db.session.query(Records).filter(Records.user_id == g.user.id,Records.question_answer_id == questionId).update({Records.user_answer_content: text_value, Records.user_answer_filepath: filepath})
    #             # 更新记录
    #             db.session.query(Records).filter(
    #                 Records.user_id == g.user.id,
    #                 Records.question_answer_id == questionId
    #             ).update({
    #                 Records.user_answer_content: text_value,
    #                 Records.user_answer_path: filepath
    #             })
    #
    #             # 提交更改到数据库
    #             db.session.commit()


@app.route('/submit_answers_test',methods = ['GET','POST'])
def submit_answers_test():
    print('-----------------------save_answers-----------------------')
    if request.method == 'POST':
        # 处理表单文本数据
        text_data = request.form.to_dict()  # 包含了问题ID和相应的文本答案

        # 处理文件上传
        files = request.files.to_dict()  # 包含了问题ID和相应的文件对象
        questionIDs = []
        for question_id_text, text_value in text_data.items():
            print(f'问题ID：{question_id_text}，文本答案：{text_value}')
            question_id = question_id_text.split('-')[-1]
            questionIDs.append(question_id)

            # input('-----------------------input-----------------------' )
            # 对应问题的文件对象
            file = files.get(f'file-{question_id}')  # 假设前端字段名为'file-问题ID'

            filepath = None
            if file and file.filename:
                # 保存文件到服务器的上传文件夹
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                print(f'文件已保存到：{filepath}')

            # 在这里进行数据库更新操作
            # 假设 g.user.id 包含了当前用户的ID，确保你的应用有途径获取当前用户ID
            user_id = g.user.id  # 示例用户ID，根据实际情况获取

            # 查找或创建数据库记录
            record = db.session.query(Records).filter(
                Records.user_id == user_id,
                Records.question_answer_id == question_id
            ).first()

            if not record:
                # 如果没有找到记录，则创建新记录
                record = Records(
                    user_id=user_id,
                    question_answer_id=question_id,
                    user_answer_content=text_value,
                    user_answer_path=filepath
                )
                db.session.add(record)
            else:
                # 如果找到了记录，则更新记录
                record.user_answer_content = text_value
                record.user_answer_path = filepath

            # 提交更改到数据库
            db.session.commit()

        # 返回一个成功的响应
        return jsonify(code=200, message='保存成功！',question_ids=questionIDs)


# def submit_answer():
#     print('-----------------------submit_answer-----------------------')
#     # id = request.args.get('id')
#     # print('-----------------------id-----------------------')
#     # print(id)
#     # # 查询数据库获取题目信息
#     # question = QuestionAnswerModel.query.get(id)
#     # if question:
#     #     # 如果找到了题目，将题目信息传递给模板进行渲染
#     #     return render_template('titleview.html', question=question)
#     # else:
#     #     # 如果未找到题目，可以返回一个错误页面或者重定向到其他页面
#     #     return render_template('error.html', message='题目不存在')
#
#     # 解析JSON数据
#     # print(request)
#     # print(type(request))
#     # print(request)
#     # input('-----------------------input-----------------------')
#     # # print(request.json)
#     # if request.method == 'POST':
#     #     print('-----------------------POST-----------------------')
#     # if request.method == 'GET':
#     #     print('-----------------------GET-----------------------')
#     # data = request.Formdata
#     # text_value = data.get('textValue')
#     # image_files = data.get('imageFiles')
#     # print('-----------------------textValue-----------------------')
#     # print(text_value)
#     # print('-----------------------imageFiles-----------------------')
#     # print(image_files)
#
#     if request.method == 'POST':
#         value = request.form
#         print(f'-----------------------value:{value}-----------------------')
#         text_value = request.form.get('textValue')
#
#         image_files = request.files.getlist('imagesFiles[0]')
#
#         print('-----------------------textValue-----------------------')
#         print(text_value)
#         print('-----------------------imageFiles-----------------------')
#         print(image_files)
#     input('-----------------------input-----------------------')
#
#
#     # 处理文本值
#     # 在这里你可以对 text_value 进行进一步的处理，比如存储到数据库中
#
#     # 处理图片文件
#     # image_paths = []
#     # for file in image_files:
#     #     if file and allowed_file(file['name']):
#     #         filename = secure_filename(file['name'])
#     #         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     #         file_data = file['data'].split(',')[1]  # 提取base64编码中的数据部分
#     #         with open(filepath, 'wb') as f:
#     #             f.write(file_data.decode('base64'))  # 解码base64并写入文件
#     #         image_paths.append(filepath)
#
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part','code':400})
#                 # return redirect(request.url)
#
#     file = request.files['file']
#
#     if file.filename == '':
#         return jsonify({'error': 'No selected file','code':400})
#         # return redirect(request.url)
#
#
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         ## Save image information to the database
#         ## 判断用户是否有图片  有就更新  没有就添加
#     print('-----------------------filepathd-----------------------')
#     print(filepath)
#     # if Records.query.filter_by(user_id=g.user.id).first().user_answer_content:  ##'default.jpg'
#     #     pass
#     # else:
#     #     # record = Records(user_answer_content=TextValue, user_answer_filepath=filepath, user_id=g.user.id)
#     #     record = Records(user_answer_content=TextValue,user_id=g.user.id)
#     #     db.session.add(record)
#     #     db.session.commit()
#     return jsonify({'message': 'File uploaded successfully', 'filepath': filepath})
#     # print('-----------------------image_paths-----------------------')
#     # print(image_paths)
#     #
#     # # 响应成功信息
#     # return jsonify({'code': 200, 'message': '提交成功！', 'image_paths': image_paths})
#     # if request.method=='GET':
#     #     if 'file' not in request.files:
#     #         return jsonify({'error': 'No file part'})
#     #
#     #     file = request.files['file']
#     #
#     #     if file.filename == '':
#     #         return jsonify({'error': 'No selected file'})
#     #
#     #     # 读取文件内容
#     #     file_data = file.read()
#     #
#     #     # 创建图片对象并保存到数据库
#     #     new_image = Image(name=file.filename, data=file_data)
#     #     db.session.add(new_image)
#     #     db.session.commit()
#     #
#     #     return jsonify({'message': 'File uploaded successfully'})
#         # print('-----------------------GET-----------------------')
#         # data = request.get_json()
#         # textValue = data.get('textValue')
#         # print('-----------------------textValue-----------------------')
#         # print(textValue)
#         # imageFiles = data.get('imageFiles')
#         # print('-----------------------imageFiles-----------------------')
#         # print(imageFiles)
#         # input('-----------------------input-----------------------')
#         # return jsonify({'code': 200, 'message': '提交成功'})
#
#
#
#
#
#     return render_template('titleview.html')
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



