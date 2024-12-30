from flask_wtf import FlaskForm  # Flask-WTF 是一個簡化表單處理的擴展，提供驗證和其他功能
from flask_wtf.file import FileField, FileAllowed  # 用於處理文件上傳的字段和文件格式驗證
from flask_login import current_user  # 提供當前登錄用戶的上下文信息
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField  # 表單字段類型
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  # 用於字段的驗證器
from flaskblog.models import User  # 引入用戶模型以便在表單中進行資料庫驗證

# 註冊表單類別，繼承自 FlaskForm
class RegistrationForm(FlaskForm):
    # 定義用戶名稱欄位
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])  # 必填，長度限制在2到20之間
    # 定義電子郵件欄位
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  # 必填，並且需要是有效的電子郵件地址格式
    # 定義密碼欄位
    password = PasswordField('Password', validators=[DataRequired()])  # 必填
    # 定義確認密碼欄位
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])  # 必填，且必須與密碼一致
    # 定義提交按鈕
    submit = SubmitField('Sign Up')  # 用於提交表單

    # 用戶名驗證方法，用於檢查用戶名稱是否已被使用
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()  # 查詢資料庫中是否有相同用戶名
        if user:  # 如果找到匹配的用戶
            raise ValidationError('That username is taken. Please choose a different one.')  # 拋出錯誤信息

    # 電子郵件驗證方法，用於檢查電子郵件是否已被使用
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()  # 查詢資料庫中是否有相同電子郵件
        if user:  # 如果找到匹配的用戶
            raise ValidationError('That email is taken. Please choose a different one.')  # 拋出錯誤信息


# 登入表單類別
class LoginForm(FlaskForm):
    # 定義電子郵件欄位
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  # 必填，並且需要是有效的電子郵件地址格式
    # 定義密碼欄位
    password = PasswordField('Password', validators=[DataRequired()])  # 必填
    # 定義記住我選項
    remember = BooleanField('Remember Me')  # 用於選擇是否記住用戶的登入狀態
    # 定義提交按鈕
    submit = SubmitField('Login')  # 用於提交表單


# 更新帳戶資訊的表單類別
class UpdateAccountForm(FlaskForm):
    # 定義用戶名稱欄位
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])  # 必填，長度限制在2到20之間
    # 定義電子郵件欄位
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  # 必填，並且需要是有效的電子郵件地址格式
    # 定義用戶頭像上傳欄位
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])  
    # 僅允許上傳 jpg 和 png 格式的文件
    # 定義提交按鈕
    submit = SubmitField('Update')  # 用於提交表單

    # 用戶名驗證方法，用於檢查更新的用戶名是否已被使用
    def validate_username(self, username):
        if username.data != current_user.username:  # 如果新用戶名與當前用戶名不同
            user = User.query.filter_by(username=username.data).first()  # 查詢資料庫中是否有相同用戶名
            if user:  # 如果找到匹配的用戶
                raise ValidationError('That username is taken. Please choose a different one.')  # 拋出錯誤信息

    # 電子郵件驗證方法，用於檢查更新的電子郵件是否已被使用
    def validate_email(self, email):
        if email.data != current_user.email:  # 如果新電子郵件與當前電子郵件不同
            user = User.query.filter_by(email=email.data).first()  # 查詢資料庫中是否有相同電子郵件
            if user:  # 如果找到匹配的用戶
                raise ValidationError('That email is taken. Please choose a different one.')  # 拋出錯誤信息


# 文章表單類別，用於創建或編輯文章
class PostForm(FlaskForm):
    # 定義文章標題欄位
    title = StringField('Title', validators=[DataRequired()])  # 必填
    # 定義文章內容欄位
    content = TextAreaField('Content', validators=[DataRequired()])  # 必填
    # 定義提交按鈕
    submit = SubmitField('Post')  # 用於提交表單
