import os
import secrets
from PIL import Image  # 用於處理圖片
from flask import render_template, url_for, flash, redirect, request, abort  # Flask 的核心功能
from flaskblog import app, db, bcrypt  # 導入應用、資料庫和加密工具
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm  # 表單類別
from flaskblog.models import User, Post  # 資料庫模型
from flask_login import login_user, current_user, logout_user, login_required  # 用戶登入相關工具

# 首頁路由
@app.route("/")
@app.route("/home")
def home():
    # 查詢所有文章，並顯示於首頁
    posts = Post.query.all()
    return render_template('home.html', posts=posts)  # 將查詢的文章傳遞到 home.html 模板中

# 關於頁面路由
@app.route("/about")
def about():
    # 返回關於頁面模板，並設置標題參數
    return render_template('about.html', title='About')

# 註冊頁面路由
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # 如果用戶已登入，則直接跳轉到首頁
        return redirect(url_for('home'))
    form = RegistrationForm()  # 初始化註冊表單
    if form.validate_on_submit():  # 驗證表單是否有效
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # 將密碼加密處理
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # 創建新的用戶對象
        db.session.add(user)  # 將用戶數據添加到資料庫
        db.session.commit()  # 提交資料庫變更
        flash('Your account has been created! You are now able to log in', 'success')  # 顯示成功訊息
        return redirect(url_for('login'))  # 跳轉到登入頁面
    return render_template('register.html', title='Register', form=form)  # 顯示註冊頁面

# 登入頁面路由
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # 如果用戶已登入，則跳轉到首頁
        return redirect(url_for('home'))
    form = LoginForm()  # 初始化登入表單
    if form.validate_on_submit():  # 驗證表單是否有效
        user = User.query.filter_by(email=form.email.data).first()  # 查詢用戶是否存在
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # 驗證密碼是否正確
            login_user(user, remember=form.remember.data)  # 登入用戶，並記住登入狀態
            next_page = request.args.get('next')  # 檢查是否有目標頁面
            return redirect(next_page) if next_page else redirect(url_for('home'))  # 跳轉到目標頁或首頁
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')  # 顯示錯誤訊息
    return render_template('login.html', title='Login', form=form)  # 顯示登入頁面

# 登出路由
@app.route("/logout")
def logout():
    logout_user()  # 執行登出操作
    return redirect(url_for('home'))  # 跳轉到首頁

# 儲存圖片函數
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # 生成隨機的 16 進制字符串作為文件名
    _, f_ext = os.path.splitext(form_picture.filename)  # 獲取文件的副檔名
    picture_fn = random_hex + f_ext  # 組合新的文件名
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)  # 文件保存路徑

    output_size = (125, 125)  # 定義圖片輸出的大小
    i = Image.open(form_picture)  # 打開圖片
    i.thumbnail(output_size)  # 調整圖片大小
    i.save(picture_path)  # 保存圖片到指定路徑

    return picture_fn  # 返回文件名

# 用戶帳號頁面路由
@app.route("/account", methods=['GET', 'POST'])
@login_required  # 確保只有登入用戶可以訪問

def account():
    form = UpdateAccountForm()  # 初始化帳號更新表單
    if form.validate_on_submit():  # 驗證表單是否有效
        if form.picture.data:  # 如果有上傳頭像，則處理圖片
            picture_file = save_picture(form.picture.data)  # 儲存頭像
            current_user.image_file = picture_file  # 更新用戶的頭像文件
        current_user.username = form.username.data  # 更新用戶名
        current_user.email = form.email.data  # 更新用戶郵件
        db.session.commit()  # 提交資料庫變更
        flash('Your account has been updated!', 'success')  # 顯示成功訊息
        return redirect(url_for('account'))  # 跳轉到帳號頁面
    elif request.method == 'GET':  # 如果是 GET 請求，預設表單值為當前用戶資訊
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # 獲取頭像文件路徑
    return render_template('account.html', title='Account', image_file=image_file, form=form)  # 顯示帳號頁面

# 新增文章路由
@app.route("/post/new", methods=['GET', 'POST'])
@login_required  # 確保只有登入用戶可以訪問

def new_post():
    form = PostForm()  # 初始化文章表單
    if form.validate_on_submit():  # 驗證表單是否有效
        post = Post(title=form.title.data, content=form.content.data, author=current_user)  # 創建新的文章對象
        db.session.add(post)  # 添加文章到資料庫
        db.session.commit()  # 提交資料庫變更
        flash('Your post has been created!', 'success')  # 顯示成功訊息
        return redirect(url_for('home'))  # 跳轉到首頁
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')  # 顯示新增文章頁面

# 顯示單篇文章內容路由
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)  # 根據文章 ID 查詢文章
    return render_template('post.html', title=post.title, post=post)  # 顯示文章頁面

# 更新文章路由
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required  # 確保只有登入用戶可以訪問

def update_post(post_id):
    post = Post.query.get_or_404(post_id)  # 查詢文章
    if post.author != current_user:  # 確保只有作者可以修改文章
        abort(403)  # 如果不是作者，返回 403 錯誤
    form = PostForm()  # 初始化文章表單
    if form.validate_on_submit():  # 驗證表單是否有效
        post.title = form.title.data  # 更新文章標題
        post.content = form.content.data  # 更新文章內容
        db.session.commit()  # 提交資料庫變更
        flash('Your post has been updated!', 'success')  # 顯示成功訊息
        return redirect(url_for('post', post_id=post.id))  # 跳轉到文章頁面
    elif request.method == 'GET':  # 如果是 GET 請求，預設表單值為文章內容
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')  # 顯示更新文章頁面

# 刪除文章路由
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required  # 確保只有登入用戶可以訪問

def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # 查詢文章
    if post.author != current_user:  # 確保只有作者可以刪除文章
        abort(403)  # 如果不是作者，返回 403 錯誤
    db.session.delete(post)  # 刪除文章
    db.session.commit()  # 提交資料庫變更
    flash('Your post has been deleted!', 'success')  # 顯示成功訊息
    return redirect(url_for('home'))  # 跳轉到首頁
