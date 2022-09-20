from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

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

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)