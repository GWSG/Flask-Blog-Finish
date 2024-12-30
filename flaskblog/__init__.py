# 匯入必要的模組與函式
from flask import Flask  # 建立 Flask 應用程式實例
from flask_sqlalchemy import SQLAlchemy  # 提供 SQL 資料庫操作功能
from flask_bcrypt import Bcrypt  # 提供密碼加密與驗證功能
from flask_login import LoginManager  # 管理用戶登入狀態與權限
from flask_mail import Mail  # 提供電子郵件發送功能
from flaskblog.config import Config  # 匯入自定義設定檔

# 初始化 Flask 擴展模組
db = SQLAlchemy()  # 資料庫處理
bcrypt = Bcrypt()  # 密碼加密與解密
login_manager = LoginManager()  # 登入管理
#如果找不到db,就先輸入from flaskblog import db,再輸入from flaskblog import db,app
#再輸入app.app_context().push(),最後再輸入db.create_all()

login_manager.login_view = 'users.login'  # 指定未登入時的重定向頁面路由
login_manager.login_message_category = 'info'  # 設定登入提示訊息的樣式分類
mail = Mail()  # 電子郵件功能

# 應用程式工廠函數
def create_app(config_class=Config):
    app = Flask(__name__)  # 建立 Flask 應用實例
    app.config.from_object(Config)  # 從配置類載入應用設定

    # 初始化擴展功能模組
    db.init_app(app)  # 將 SQLAlchemy 資料庫綁定到應用
    bcrypt.init_app(app)  # 初始化密碼加密功能
    login_manager.init_app(app)  # 綁定登入管理器到應用
    mail.init_app(app)  # 綁定電子郵件服務到應用

    # 匯入與註冊 Blueprint
    from flaskblog.users.routes import users  # 用戶相關的路由
    from flaskblog.posts.routes import posts  # 文章相關的路由
    from flaskblog.main.routes import main  # 主頁面與靜態內容的路由
    from flaskblog.errors.handlers import errors  # 錯誤處理相關的路由

    app.register_blueprint(users)  # 註冊用戶相關的 Blueprint
    app.register_blueprint(posts)  # 註冊文章相關的 Blueprint
    app.register_blueprint(main)  # 註冊主頁面相關的 Blueprint
    app.register_blueprint(errors)  # 註冊錯誤處理相關的 Blueprint

    return app  # 返回已配置好的應用實例