from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response, session, abort
from werkzeug.routing import BaseConverter
from flask_sqlalchemy import SQLAlchemy
from client import clienttt

import pymysql
import json
import socket,struct,os



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
    #查看天气预测权限
    permission_forecast = db.Column(db.Boolean)
    #查看指定天气预测权限
    permission_search = db.Column(db.Boolean)
    #后台管理权限
    permission_master = db.Column(db.Boolean)

    #关联，返回
    users = db.relationship('User', backref='role')
    #repr（）方法显示一个可读字符串
    def __repr__(self):
        return '<角色: 角色ID:%s 角色名:%s 查看权限:%s 查询权限:%s 管理权限:%s>' % (self.id, self.name, self.permission_forecast, self.permission_search, self.permission_master)


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
        return '<用户: 用户ID:%s 用户名:%s 用户密码:%s 角色:%s>' % (self.name, self.id, self.password, self.role_id)

#设置cookie
@app.route('/set_cookie/<username>')
def set_cookie(username):
    response=make_response(redirect(url_for("login")));
    response.set_cookie('userID',username)
    session["username"] = username
    return response


#登出页
@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("login")));
    #如果是登录状态，就删除cookie和session
    if "username" in session:
        #删除session
        session.pop("username")
        #删除cookie
        response.delete_cookie('userID')
    return response


#主页
@app.route('/', methods=['GET', 'POST'])
def login():
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
        return redirect(url_for('permission'))


#注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('UserName')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')
        if username and password1 and password2:
            #两次输入密码一样
            if password1 == password2:
                user = User.query.filter(User.name == username).first()
                #用户不存在
                if not user:
                    try:
                        #将用户添加到数据库
                        user = User(name=username,password=password1,role_id=role1.id)
                        db.session.add(user)
                        db.session.commit()
                        #返回主页
                        return redirect(url_for('login'))
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
    date="null";
    weather_data = [];
    if request.method == 'POST':
        #获取日期
        date = request.form.get('date')
        Date=date.split("-")
        year = int(Date[0])
        month = int(Date[1])
        day = int(Date[2])
        date = str(month) + '#' + str(day)
    #如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('login'))
    #如果登录，就读取cookie并前往数据预测页
    else:
        #userID = request.cookies.get('userID')
        #使用session获取用户名
        userID = session.get('username')
        user = User.query.filter(User.name == userID).first()
        role = Role.query.filter(Role.id == user.role_id).first()
        #赋值权限
        permission_list = {'forecast': False, 'search': False, 'master': False}
        permission_list['forecast'] = role.permission_forecast
        permission_list['search'] = role.permission_search
        permission_list['master'] = role.permission_master

        #检测是否有搜索权限，如果有就查询是否有查询的日期
        if permission_list['search']:
            # 请求数据
            if date != "null":
                print(date)
                # 读取数据
                with open('static/data/receive.json', 'r') as f:
                    data = json.load(f)
            #如果没有日期，就显示预订数据
            else:
                with open('static/data/today.json', 'r') as f:
                    data = json.load(f)
        #如果没有搜索权限，就显示服务器的预订数据
        else:
            with open('static/data/today.json', 'r') as f:
                data = json.load(f)
        #将数据存入列表
        for i in data:
            weather_data.append(int(data[i]))
        return render_template('prediction.html',userID=userID,data_min=weather_data,data_max=weather_data,permission_list=permission_list)

#更改密码页面
@app.route('/changepasswordadmin/<change_user>', methods=['GET', 'POST'])
def changepasswordadmin(change_user):
    if request.method == 'POST':
        #获取日期
        change_password = request.form.get('password')
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('login'))
    # 如果登录，就读取cookie并前往页面
    else:
        userID = session.get('username')
        user = User.query.filter(User.name == userID).first()
        role = Role.query.filter(Role.id == user.role_id).first()
        if role.permission_master:
            user = User.query.filter(User.name == change_user).first()
            if user:
                try:
                    # 更改用户密码
                    user.password = change_password
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
            return redirect(url_for('settingadmin',user_name=userID))
        else:
            return redirect(url_for('logout'))

#更改权限页面
@app.route('/changeroleadmin/<change_user>', methods=['GET', 'POST'])
def changeroleadmin(change_user):
    if request.method == 'POST':
        #获取日期
        roleid = request.form.get('roleid')
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('login'))
    # 如果登录，就读取cookie并前往页面
    else:
        userID = session.get('username')
        user = User.query.filter(User.name == userID).first()
        role = Role.query.filter(Role.id == user.role_id).first()
        if role.permission_master:
            user = User.query.filter(User.name == change_user).first()
            if user:
                try:
                    # 更改用户密码
                    user.role_id = roleid
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
            return redirect(url_for('settingadmin',user_name=userID))
        else:
            return redirect(url_for('logout'))

#删除用户页面
@app.route('/deleteuseradmin/<change_user>', methods=['GET', 'POST'])
def deleteuseradmin(change_user):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('login'))
    # 如果登录，就读取cookie并前往页面
    else:
        userID = session.get('username')
        user = User.query.filter(User.name == userID).first()
        role = Role.query.filter(Role.id == user.role_id).first()
        if role.permission_master:
            user = User.query.filter(User.name == change_user).first()
            if user:
                try:
                    db.session.delete(user)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
            return redirect(url_for('settingadmin',user_name=userID))
        else:
            return redirect(url_for('logout'))

#注册页面
@app.route('/createuseradmin', methods=['GET', 'POST'])
def createuseradmin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        roleid = request.form.get('roleid')
        # 如果没有登录，就返回登录页
        if "username" not in session:
            return redirect(url_for('login'))
        # 如果登录，就读取cookie并前往页面
        else:
            userID = session.get('username')
            user = User.query.filter(User.name == userID).first()
            role = Role.query.filter(Role.id == user.role_id).first()
            createuser = User.query.filter(User.name == username).first()
            if role.permission_master:
                if username and password and roleid:
                    #用户不存在
                    if not createuser:
                        try:
                            #将用户添加到数据库
                            createuser = User(name=username,password=password,role_id=roleid)
                            db.session.add(createuser)
                            db.session.commit()
                        except Exception as e:
                            print(e)
                            flash('用户创建操作失败！')
                            db.session.rollback()
                    else:
                        flash('同样的账户名存在！')
                else:
                    flash('输入框不能为空！')
    return redirect(url_for('settingadmin',user_name=userID))

#管理员页面
@app.route('/settingadmin/<user_name>', methods=['GET', 'POST'])
def settingadmin(user_name):
    flash('输入信息')
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('login'))
    # 如果登录，就读取cookie并前往数据预测页
    else:
        userID = session.get('username')
        if user_name == userID:
            user = User.query.filter(User.name == userID).first()
            role = Role.query.filter(Role.id == user.role_id).first()
            if role.permission_master:
                users = User.query.all()
                roles = Role.query.all()
                return render_template('admin.html',users=users,roles=roles,user_name=userID)
            else:
                return redirect(url_for('logout'))
        else:
            return redirect(url_for('logout'))

#用户页面
@app.route('/settinguser/<user_name>', methods=['GET', 'POST'])
def settinguser(user_name):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('login'))
    # 如果登录，就读取cookie并前往数据预测页
    else:
        userID = session.get('username')
        if user_name == userID:
            user = User.query.filter(User.name == userID).first()
            role = Role.query.filter(Role.id == user.role_id).first()
            return render_template('user.html',user=user, role=role,user_name=userID)
        else:
            return redirect(url_for('logout'))

#权限判断页面
@app.route('/permission', methods=['GET', 'POST'])
def permission():
    #获取用户名
    username = session.get('username')
    return redirect(url_for('prediction'))



#初始化测试函数
def init():
    #删除表
    db.drop_all()
    #创建表
    db.create_all()
    #创建权限表
    role1 = Role(name='管理员',permission_forecast=True,permission_search=True,permission_master=True)
    role2 = Role(name='普通用户',permission_forecast=True,permission_search=True,permission_master=False)
    role3 = Role(name='VIP用户', permission_forecast=True,permission_search=False,permission_master=False)
    db.session.add(role1)
    db.session.add(role2)
    db.session.add(role3)
    db.session.commit()
    #添加两个用户
    user1 = User(name='test1',password='123456',role_id=role1.id)
    user2 = User(name='test2', password='123456', role_id=role2.id)
    user3 = User(name='test3', password='123456', role_id=role3.id)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()


#启动服务器
if __name__ == '__main__':
    init()
    app.run(debug=True)