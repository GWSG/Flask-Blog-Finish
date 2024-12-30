# 導入 Flask-WTF 和 WTForms 的必要模組
from flask_wtf import FlaskForm  # Flask-WTF 提供簡化表單操作的擴展
from wtforms import StringField, SubmitField, TextAreaField  # 定義表單字段的類
from wtforms.validators import DataRequired  # 驗證器，用於確保字段不為空

# 定義文章表單類
class PostForm(FlaskForm):  
    # 繼承 FlaskForm，表示這是一個表單類
    
    # 定義標題字段
    title = StringField('Title', validators=[DataRequired()])  
    # 字符串輸入字段，標籤為 'Title'
    # 使用 DataRequired 驗證器，確保此字段為必填項

    # 定義內容字段
    content = TextAreaField('Content', validators=[DataRequired()])  
    # 多行文本輸入字段，標籤為 'Content'
    # 使用 DataRequired 驗證器，確保此字段為必填項

    # 定義提交按鈕
    submit = SubmitField('Post')  
    # 按鈕，用於提交表單，標籤為 'Post'
