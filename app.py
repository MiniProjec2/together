from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta

import jwt
import hashlib

app = Flask(__name__)
client = MongoClient('mongodb+srv://text:sparta@cluster0.cvfqh2o.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/')
def login():
    return render_template('login.html')
@app.route('/login/api')
def login_api():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    
    pw_hash = hashlib.sha256(pw_receive.encode('utf8')).hexdigest()
    
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
    
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60*60*1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/category/create')
def postIndex():
    return render_template('postIndex.html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)