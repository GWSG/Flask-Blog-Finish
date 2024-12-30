from datetime import datetime  # 用於處理日期與時間，例如設置文章的發佈時間戳
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # 用於生成和驗證加密令牌（如密碼重設令牌）
from flask import current_app  # 提供對當前 Flask 應用配置的訪問
from flaskblog import db, login_manager  # 從應用導入資料庫對象和登入管理器
from flask_login import UserMixin  # 提供用戶模型的基本功能，如驗證

@login_manager.user_loader  # 為登入管理器定義一個回調函數
def load_user(user_id):  # 該函數在需要加載用戶時被調用
    return User.query.get(int(user_id))  # 根據用戶 ID 查詢資料庫並返回對應的用戶對象

# 定義 User 類，表示資料庫中的 user 表，並繼承 Flask-Login 的 UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # 唯一主鍵，用於標識用戶
    username = db.Column(db.String(20), unique=True, nullable=False)  # 用戶名，必須唯一且不可為空
    email = db.Column(db.String(120), unique=True, nullable=False)  # 電子郵件地址，必須唯一且不可為空
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # 頭像文件，默認為 default.jpg
    password = db.Column(db.String(60), nullable=False)  # 密碼字段，存儲加密後的密碼
    posts = db.relationship('Post', backref='author', lazy=True)  # 與文章表的關聯，一對多關係

    def get_reset_token(self, expires_sec=1800):  # 生成密碼重設令牌，默認有效期為 30 分鐘
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)  # 使用應用的 SECRET_KEY 進行加密
        return s.dumps({'user_id': self.id}).decode('utf-8')  # 將用戶 ID 加密並返回令牌

    @staticmethod  # 定義靜態方法，不需要對象實例即可調用
    def verify_reset_token(token):  # 驗證密碼重設令牌
        s = Serializer(current_app.config['SECRET_KEY'])  # 使用應用的 SECRET_KEY 進行解密
        try:
            user_id = s.loads(token)['user_id']  # 解密令牌，提取用戶 ID
        except:
            return None  # 如果解密失敗，返回 None
        return User.query.get(user_id)  # 根據解密的用戶 ID 查詢用戶對象

    def __repr__(self):  # 定義對象的字符串表示，用於調試
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# 定義 Post 類，表示資料庫中的 post 表
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 唯一主鍵，用於標識文章
    title = db.Column(db.String(100), nullable=False)  # 文章標題，最大長度 100 且不可為空
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 發佈日期，默認為當前 UTC 時間
    content = db.Column(db.Text, nullable=False)  # 文章內容，不可為空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外鍵，指向用戶表的 ID

    def __repr__(self):  # 定義對象的字符串表示，用於調試
        return f"Post('{self.title}', '{self.date_posted}')"
