from crypt import methods
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_from_directory
from pymongo import MongoClient  
from bson import ObjectId
import jwt
import requests
# from werkzeug.utils import secure_filename
# import os

app = Flask(__name__)
# client = MongoClient('mongodb://test:test@18.233.169.28', 27017)
client = MongoClient('localhost', 27017)
db = client.dbsample

#처음 메인 페이지 들어왔을때 세션을 통해 로그인 되어있는지 안되어있는지 확인
@app.route('/')
def home():
   # session['logged_in'] = False
   if session.get('logged_in'):
      now_name = session['membername']
      print(now_name+"!!!!!!!!!!")
      return render_template('login.html')
   else:
      return render_template('login.html')
   # if session.get('logged_in'):
   #    #세션에서 회원 이름 받아와 뿌려주기

   #    now_name = session['membername']
   #    now_pk = session['membername']
   #    # return jsonify({'result': 'success', 'data': name})
   #    return render_template('main.html', username = now_name, pk = now_pk)
   # else:
   #    return render_template('main.html')

@app.route('/regi')
def regi1():
    return render_template('main.html')


#로그인 모달창 로그인 버튼
@app.route('/login', methods=['POST'])
def login():
   #매개변수로 아이디, 패스워드 받기

   userid = request.form['id_give']
   password = request.form['password_give']
   user = db.dbsample.find_one({'userid':userid})
   if user:
      
      db_password = jwt.decode(user['password'], 'abcde', algorithms=['HS256'])['password']
      # 나중에 try, catch로 구현할 생각 jwt.decode("JWT_STRING", "secret", algorithms=["HS256"])
      if password == db_password:
         session['logged_in'] = True
         #dbsample 디비에서 유저아이디로 찾은 유저 네임을 /home에서 뿌려줄꺼임
         cname = db.dbsample.find_one({'userid':userid})
         session['membername'] = cname['username']

         #pk_key 값도 안보이지만 넘겨줄거에요
         #pk_key = ObjectId(cname['_id'])
         #session['member_pk'] = pk_key
         #최신 등록순으로 뿌려주기 위해
         #session['sort_order'] = 'time'
         return jsonify({'result': 'success'})
   return jsonify({'result': 'fail'})

# 로그아웃 시 처리해야함

@app.route('/logout', methods=['GET'])

def logout():
   session['logged_in'] = False
   return jsonify({'result':'success'})

#회원가입 모달창 회원가입 버튼
@app.route('/register', methods=['POST'])
def add_user():
   #JWT로 암호화 하지 않은 비번
   before_password = request.form['password_give']
   after_password = jwt.encode({'password': before_password}, 'abcde', algorithm='HS256')
   
   # 파라미터로 받은 이름, 아이디, 암호화된 비번을 json형식으로 묶어놈
   user_name = request.form['name_give']
   new_user = {'username':user_name, 'userid':request.form['id_give'], 'password': after_password}
   db.dbsample.insert_one(new_user)
   return jsonify({'result': 'success'})
   
#회원가입 모달창 아이디 중복 검사 버튼 
@app.route('/sameid', methods=['POST'])
def same_id():
   userid = request.form['id_give']
   if list(db.dbsample.find({'userid':request.form['id_give']})):
      return jsonify({'result': 'overlap'})
   else:
      return jsonify({'result': 'success'})

@app.route('/myprofile', methods=['POST'])
def my_profile():
   
   user_id = request.form['id_give']
   
   return render_template('myprofile.html', )

# @app.route('/uploader', methods=['GET','POST'])
# def uploader_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       #os.path.join(app.config['UPLOAD_FOLDER']
#       f.save('/Users/angel/Documents/week00/jungle_week0/static', secure_filename(f.filename))
#       return 'file uploaded successfully'


if __name__ == '__main__':
   app.secret_key = "123"
   app.run('0.0.0.0',port=5000,debug=True)