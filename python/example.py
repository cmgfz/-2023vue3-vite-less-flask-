from flask import Flask,jsonify
from flask import request
from flask import abort,redirect
import json
app=Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello,World'

@app.route('/hey/<username>')
def hei_yingong(username):
    return 'hey %s'%username

@app.route('/hey/<int:number>')
def my_number(number):
    return 'hey %s'%(number+number)

@app.route('/baidu')
def baidu():
    return redirect("https://www.baidu.com")

@app.route("/test/my/first",methods=["POST"])
def first_post():
    try:
        my_json=request.get_json()
        print(my_json)
        get_name=my_json.get("name")
        get_age=my_json.get("age")
        if not all([get_name,get_age]):
            return jsonify(msg='缺少参数')
        get_age+=10
        return jsonify(name=get_name,age=get_age)
    except Exception as e:
        print(e)
        return jsonify(msg="出错了哦，请查看是否正确访问")



if __name__ == '__main__':
   app.run(port=int("3000"),debug=True)
