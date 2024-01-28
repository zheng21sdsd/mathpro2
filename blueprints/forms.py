import wtforms
from wtforms.validators import Email,EqualTo,Length,InputRequired
from models import UserModel
from models import EmailCaptchaModel
from exts import db


# Form 主要用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误！')])
    captcha = wtforms.StringField(validators=[Length(min = 4,max = 400,message = 'yzm错误！')])
    username = wtforms.StringField(validators=[Length(min= 2,max = 400,message='用户名错误！')])
    password = wtforms.StringField(validators=[Length(min = 2,max = 400,message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])
# 我们也可以用jquery就像获取qq邮箱一样，来获取各个表单，但这个就得一一找到input对应的id然后获取

    # 自定义验证
    #1.邮箱是否已近被注册了

    def validate_email(self,field): #//验证是否已经注册了
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        print(type(user))
        if user:
            raise wtforms.ValidationError(message='该邮箱已经被注册了')#这里的抛出错误页面信息，必须是在前端页面展示的

    # 2.验证码是否正确  注这里field是传过来的参数 就是上面的email captcha,username,password之类的
    def validate_captcha(self,field):#这里是表单类的验证验证码的函数，所以self代表表单对象
        captcha = field.data
        # EmailCaptchaModel.query.filter_by(captcha)
        email = self.email.data# 最终获得表单的email的data
        captcha_model = EmailCaptchaModel.query.filter_by(email = email,captcha = captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='验证码输入错误！')
        # else: 最好写个脚本，定期的清理一次
        #     #to da 删除验证码
        #     db.session.delete(captcha)
        #     db.session.commit()

class Loginform(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误！')])
    password = wtforms.StringField(validators=[Length(min=2, max=400, message="输入格式错误！")])

