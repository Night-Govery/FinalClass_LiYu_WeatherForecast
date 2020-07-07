from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32), unique=True)
    #外键，表明+id
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #关联需要在另一个模型中定义
    #repr（）方法显示一个可读字符串
    def __repr__(self):
        return '<User: %s %s %s>' % (self.name, self.id,self.password)



#正则表达式
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


#主页
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method ==  'POST':
        username = request.form.get('UserName')
        password = request.form.get('Password')
        user = User.query.filter(User.name == username).first()
        if user:
            if user.password == password:
                flash('登录成功！')
                return redirect(url_for('prediction',user_name=user.name))
            else:
                flash('密码错误！')
        else:
            flash('账户不存在！')
    return render_template('login.html')

'''
app.url_map.converters['re'] = RegexConverter
@app.route('/orders/<re("[0-9]{3}"):order_id>', methods=['GET','POST'])
def get_order_id(order_id):
    return "order id is %s" % order_id
    '''


@app.route('/register', methods=['GET', 'POST'])
def register():
    isRight = True
    if request.method == 'POST':
        username = request.form.get('UserName')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')
        isRight=True
    return render_template('register.html', isRight=isRight)

@app.route('/prediction/<user_name>', methods=['GET', 'POST'])
def prediction(user_name):
    return render_template('prediction.html', user_name=user_name)


#启动服务器
if __name__ == '__main__':
    #删除表
    db.drop_all()

    #创建表
    db.create_all()

    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    user1 = User(name='hhh',password='123456',role_id=role.id)
    user2 = User(name='erwer', password='23fedrwe', role_id=role.id)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()


    app.run(debug=True)