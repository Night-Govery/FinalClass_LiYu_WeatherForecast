from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.routing import BaseConverter



app = Flask(__name__)
#读取配置文件
app.config.from_pyfile('config.ini')

#正则表达式
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method ==  'POST':
        username = request.form.get('UserName')
        password = request.form.get('Password')
        #return render_template('register.html')
    return render_template('login.html')

app.url_map.converters['re'] = RegexConverter

@app.route('/orders/<re("[0-9]{3}"):order_id>', methods=['GET','POST'])
def get_order_id(order_id):
    return "order id is %s" % order_id


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

#返回json
@app.route('/demo3')
def demo3():
    return jsonify('./static/data/min.json')

@app.route('/demo4')
def demo4():
    return redirect('http://www.baidu.com')

@app.route('/demo5')
def demo5():
    return redirect(url_for('index'))
#启动服务器
if __name__ == '__main__':
    app.run()