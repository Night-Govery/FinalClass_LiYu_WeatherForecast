from flask import Flask, request

# Define the WSGI application object
app = Flask(__name__)

@app.route('/user/<user_id>')
def user_info(user_id):
    return 'hello %s' % user_id

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # 直接从请求中取到请求方式并返回
    return request.method
if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True, port=5000)