from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta

import jwt
import hashlib
import certifi

app = Flask(__name__)
client = MongoClient('mongodb+srv://text:sparta@cluster0.cvfqh2o.mongodb.net/cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta

SECRET_KEY = 'SPARTA'

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    textInfo = [
        {"text": "아이디",
         "id": "user_id"
         },
        {"text": "비밀번호",
         "id": "user_pw"
         },
    ]
    return render_template('login.html', textInfo=textInfo)

@app.route('/login/api', methods=['POST'])
def api_login():
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

@app.route('/generic', methods=['GET'])
def detail():
    return render_template('generic.html')

@app.route('/join')
def join():
    textInfo = [
        {"text": "아이디 (영문과 숫자 및 일부 특수문자(._-), 2-10자 길이)",
         "id": "user_id"
         },
        {"text": "비밀번호 (영문, 숫자는 필수이며 일부 특수 문자 사용 가능 8-20자 길이)",
         "id": "user_pw"
         },
        {"text": "비밀번호 재입력",
         "id": "user_pw_re"
         },
        {"text": "닉네임",
         "id": "user_nickname"
         },
        {"text": "Github 주소 (선택)",
         "id": "user_git"
         }
    ]
    return render_template('join.html', textInfo=textInfo)

@app.route('/join/id_check', methods=["POST"])
def user_id_check():
    idReceive = request.form['id_give']
    exists = bool(db.users.find_one({"id": idReceive}))
    return jsonify({'result:': 'success', 'exists': exists})

@app.route('/join', methods=["POST"])
def userRegister():
    idReceive = request.form['id_give']
    pwReceive = request.form['pw_give']
    nicknameReceive = request.form['nickname_give']
    gitReceive = request.form['git_give']

    pwHash = hashlib.sha256(pwReceive.encode('utf-8')).hexdigest()

    doc = {
        'id': idReceive,
        'pw': pwHash,
        'nickname': nicknameReceive,
        'git': gitReceive,
    }
    db.movies.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

@app.route('/category/create')
def postIndex():
    return render_template('postIndex.html')

@app.route("/category/create", methods=["POST"])
def postIndexCreate():
    categoryReceive = request.form['categoryGive']
    titleReceive = request.form['titleGive']
    contentReceive = request.form['contentGive']

    doc = {
        'category':categoryReceive,
        'title' :titleReceive,
        'content' :contentReceive
    }

    db.postIndex.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)