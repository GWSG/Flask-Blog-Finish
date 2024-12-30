import os  # 導入操作系統模組，用於訪問環境變數和進行文件操作

class Config:
    # 設定應用程式的密鑰，用於加密敏感數據（如 Session 資料）
    # 如果環境變數 'SECRET_KEY' 存在，使用其值，否則使用指定的預設密鑰
    SECRET_KEY = os.environ.get('SECRET_KEY', '5791628bb0b13ce0c676dfde280ba245')

    # 定義資料庫連接 URI，用於告訴 SQLAlchemy 如何連接資料庫
    # 如果環境變數 'SQLALCHEMY_DATABASE_URI' 存在，使用其值，否則預設為 SQLite 資料庫
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')

    # 關閉 SQLAlchemy 的事件通知功能，以提高效能
    # 此設置用於禁用對物件變更的追蹤
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置郵件服務器
    MAIL_SERVER = 'smtp.googlemail.com'  # Gmail 的 SMTP 伺服器地址
    MAIL_PORT = 587  # 使用 TLS 加密時的標準 SMTP 埠
    MAIL_USE_TLS = True  # 啟用傳輸層安全性（TLS）

    # 設定郵件伺服器的認證憑據
    # 如果環境變數 'EMAIL_USER' 和 'EMAIL_PASS' 存在，使用其值，否則使用預設值
    MAIL_USERNAME = os.environ.get('EMAIL_USER', 'default_email@example.com')  # 郵件帳戶名稱
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS', 'default_password')  # 郵件帳戶密碼
