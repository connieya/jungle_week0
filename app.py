from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import jwt, json, hashlib
import datetime as dt

app = Flask(__name__)
client = MongoClient('localhost',27017)
db = client.week1

SECRET_KEY = 'three'

@app.route('/home')
def home():
   return render_template('main.html')

@app.route('/')
def main():
   user_list = list(db.user.find({}))
   if "user_id" in session :
      user_id = session['user_id']
      return render_template('main.html', session_id = user_id , login = True , users = user_list)

   return render_template('main.html' , login = False , users = user_list)

   # token_receive = request.cookies.get('token')
   # id_receive = request.cookies.get('data')
   # # data = request.cookies.get('data')

   # try:
   #    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
   #    print('try')
   #    return render_template('main.html', users = user_list)

   # except jwt.ExpiredSignatureError:
   #    print('except')
   #    return redirect(url_for('home', token_expired='로그인 시간이 만료되었습니다.'))
   # except jwt.exceptions.DecodeError:
   #    print('except')
   #    return redirect(url_for('home'))


@app.route('/signUp',methods = ['POST'])
def add_user():
   before_password = request.form['user_pw']
   after_password = hashlib.sha256(before_password.encode('utf-8')).hexdigest()
   user_name  = request.form['user_name']
   user_id = request.form['user_id']
   new_user = {'user_id' : user_id , 'name' : user_name , 'password' : after_password}
   db.user.insert_one(new_user)
   return jsonify({'result' : 'success'})



@app.route('/login' , methods=['POST'])
def login() :
   login_id = request.form['login_id']
   login_pw = request.form['login_pw']
   login_after_pw = hashlib.sha256(login_pw.encode('utf-8')).hexdigest()
   user = db.user.find_one({'user_id' : login_id}, {'password': login_after_pw})
   print(user)
   if user :
      payload = {
         'id': login_id,
         'exp': dt.datetime.utcnow() + dt.timedelta(seconds=3000)
      }
      
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
      session['user_name'] = user['user_id']

      return jsonify({'result': 'success', 'token': token})

   else:
      return jsonify({'result' :'fail', 'msg': '아이디 혹은 비밀번호가 일치하지 않습니다.'})


@app.route('/logout' , methods =['GET'])
def logout():
   session.pop('user_id')
   # session['logged_in'] = False
   return jsonify({'result' : 'success'})

@app.route('/profilepage/<user_id>')
def profilePage(user_id):
   user_info = db.user.find_one({'user_id' : user_id })
   my_info = list(db.info.find({'user_id' : user_info['user_id']}))
   return render_template('myprofile.html' ,user_info = user_info , my_info = my_info)


@app.route('/registerInfo' , methods = ['POST'])
def myprofile():
   user_id  = request.form['user_id']
   my_info  = request.form['my_info']
   name  = request.form['name']
   db.info.insert_one({'user_id' : user_id ,'name' : name , 'info' : my_info})
   return jsonify({'result' : 'success'})

@app.route('/yourProfile/<user_id>')
def you(user_id):
   user_info = db.user.find_one({'user_id' : user_id })
   common_content = list(db.info.find({'user_id' : user_info['user_id']}))
   return render_template('yourprofile.html' , common_content = common_content , user_name = user_info['name'] , user_id = user_info['user_id'])


@app.route('/deleteInfo', methods=['POST'])
def deleteInfo():
   pk = request.form['pk'];
   db.info.delete_one({'_id': ObjectId(pk)})
   return jsonify({'result' : 'success'})

@app.route('/sympathy' ,  methods=['POST'])
def clickSympathy() :
   user_id = request.form['user_id'];
   person = request.form['person'];
   info = request.form['info'];
   pk = request.form['pk'];
   db.sympathy.insert_one({'id' : pk , 'user_id' : user_id , 'info' : info , 'person' : person});
   return jsonify({'result' : 'success'})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)