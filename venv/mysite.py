from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response, session, abort
from werkzeug.routing import BaseConverter
from flask_sqlalchemy import SQLAlchemy
import pymysql


pymysql.install_as_MySQLdb()
app = Flask(__name__)
#配置数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/flask_sql'
#跟踪数据库修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#加密通话
app.secret_key = '234sdqwe324234'
#创建数据库
db = SQLAlchemy(app)


#创建两张表，
# 角色表
# 用户表
#继承db.Model
class Role(db.Model):
    #定义表
    __tablename__ = 'roles'
    #定义字段
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    #关联，返回
    users = db.relationship('User', backref='role')
    #repr（）方法显示一个可读字符串
    def __repr__(self):
        return '<Role: %s %s>' % (self.name, self.id)


#数据库的用户表单
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32), unique=False)
    #外键，表明+id
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #关联需要在另一个模型中定义
    #repr（）方法显示一个可读字符串
    def __repr__(self):
        return '<User: %s %s %s>' % (self.name, self.id,self.password)


#设置cookie
@app.route('/set_cookie/<username>')
def set_cookie(username):
    response=make_response(redirect(url_for("index")));
    response.set_cookie('userID',username)
    session["username"] = username
    return response


#登出页
@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("index")));
    #如果是登录状态，就删除cookie和session
    if "username" in session:
        #删除session
        session.pop("username")
        #删除cookie
        response.delete_cookie('userID')
    return response


#主页
@app.route('/', methods=['GET', 'POST'])
def index():
    username=request.cookies.get('userID')
    if request.method ==  'POST':
        username = request.form.get('UserName')
        password = request.form.get('Password')
        user = User.query.filter(User.name == username).first()
        if user:
            if user.password == password:
                flash('登录成功！')
                #进入到添加cookie页
                return redirect(url_for('set_cookie',username=username))
            else:
                flash('密码错误！')
        else:
            flash('账户不存在！')
    #检测session是否存在“username”项
    if "username" not in session:
        #如果没有username，则进入登录页
        return render_template('login.html')
    else:
        #如果有，则证明已经登录，进入预测页
        return redirect(url_for('prediction'))


#注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('UserName')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')
        js_variable = request.form
        print(js_variable)
        if username and password1 and password2:
            #两次输入密码一样
            if password1 == password2:
                user = User.query.filter(User.name == username).first()
                #用户不存在
                if not user:
                    try:
                        #将用户添加到数据库
                        user = User(name=username,password=password1,role_id=role.id)
                        db.session.add(user)
                        db.session.commit()
                        #返回主页
                        return redirect(url_for('index'))
                    except Exception as e:
                        print(e)
                        flash('用户创建操作失败！')
                        db.session.rollback()
                else:
                    flash('同样的账户名存在！')
            else:
                flash('两次输入密码不一致！')
        else:
            flash('输入框不能为空！')

    return render_template('register.html')


#预测界面
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    #如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    #如果登录，就读取cookie并前往数据预测页
    else:
        #userID = request.cookies.get('userID')
        #使用session获取用户名
        userID = session.get('username')
        return render_template('prediction.html',userID=userID)


#初始化测试函数
def init():
    #删除表
    db.drop_all()
    #创建表
    db.create_all()
    #创建权限表
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()
    #添加两个用户
    user1 = User(name='hhh',password='123456',role_id=role.id)
    user2 = User(name='erwer', password='23fedrwe', role_id=role.id)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()


#启动服务器
if __name__ == '__main__':
    init()
    app.run(debug=True)