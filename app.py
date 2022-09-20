from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
import hashlib
from pymongo import MongoClient
client = MongoClient('mongodb+srv://text:sparta@cluster0.cvfqh2o.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/category/create')
def postIndex():
    return render_template('postIndex.html')

# -----------------------------
# 회원가입 페이지(join.html)을 불러올 때 textInfo Array에 Input Text 값을 넣어서 보내줌
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

# 아이디 중복 여부 체크, 입력 받은 아이디 값을 가져와 db에 같은 값이 있는지 확인하여 boolean 값으로 돌려줌
@app.route('/join/id_check', methods=["POST"])
def userIdCheck():
    idReceive = request.form['id_give']
    exists = bool(db.user.find_one({"id": idReceive}))
    return jsonify({'result:': 'success', 'exists': exists})

# 닉네임 중복 여부 체크, 위와 동일
@app.route('/join/nickname_check', methods=["POST"])
def userNicknameCheck():
    nicknameReceive = request.form['nickname_give']
    exists = bool(db.user.find_one({"nickname": nicknameReceive}))
    return jsonify({'result:': 'success', 'exists': exists})

# 회원 정보를 받아와서 비밀번호는 해쉬맵으로 암호화한 뒤에 db에 저장
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
    db.user.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)