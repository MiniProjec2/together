from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@sparta.4upidwa.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('postIndex.html')

@app.route("/category/post/create", methods=["POST"])
def postIndex():
    categoryReceive = request.form['categoryGive']
    titleReceive = request.form['titleGive']
    contentReceive = request.form['contentGive']

    doc = {
        'category':categoryReceive,
        'title' :titleReceive,
        'content' :contentReceive
    }

    db.postIndex.insert_one(doc)

    return jsonify({'msg': 'POST(기록) 연결 완료!'})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)