from ast import If
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import jwt, json, hashlib
import datetime as dt

app = Flask(__name__)
client = MongoClient('localhost',27017)
db = client.week1

SECRET_KEY = 'threeeeee'

# @app.route('/home')
# def home():
#    return render_template('main.html')

@app.route('/')
def main():

   token_receive = request.cookies.get('token')
   
   user_list = list(db.user.find({}))
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      print("try")
      if "user_id" in session :
         user_id = session['user_id']
         return render_template('main.html', session_id = user_id , login = True , users = user_list)

   except jwt.ExpiredSignatureError:
      print("except")
      return render_template('main.html' , login = False , users = user_list)
   except jwt.exceptions.DecodeError:
      print("except")
      return render_template('main.html' , login = False , users = user_list)

@app.route('/idOverlap', methods=['POST'])
def same_id():
   if list(db.user.find({'user_id' :request.form['log_id']})):
      print("aaaaaa")
      return jsonify({'result': 'overlap'})
   else:
      return jsonify({'result': 'success'})


@app.route('/signUp',methods = ['POST'])
def add_user():
   before_password = request.form['user_pw']
   after_password = jwt.encode({'password' : before_password} , 'abcde' , algorithm = 'HS256')
   user_name  = request.form['user_name']
   user_id = request.form['user_id']
   d = dt.datetime.now()
   t = str(d.year) + str(d.month) + str(d.day) + str(d.hour) + str(d.minute) + str(d.second)
   timenow = int(t)
   new_user = {'user_id' : user_id , 'name' : user_name , 'password' : after_password, 'time' : timenow , 'sympathyCount' : 0}
   db.user.insert_one(new_user)
   return jsonify({'result' : 'success'})




@app.route('/login' , methods=['POST'])
def login() :
   login_id = request.form['login_id']
   login_pw = request.form['login_pw']
   login_after_pw = hashlib.sha256(login_pw.encode('utf-8')).hexdigest()
   user = db.user.find_one({'user_id' : login_id})
   print(user)
   if user :
      payload = {
         'id': login_id,
         'exp': dt.datetime.utcnow() + dt.timedelta(seconds=8600)
      }
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
      # session['user_name'] = user['user_id']
      session['logged_in'] = True
      session['user_id'] = login_id
      session['user_name'] = user['name']

      return jsonify({'result': 'success', 'token': token})

   else:
      return jsonify({'result' :'fail', 'msg': '아이디 혹은 비밀번호가 일치하지 않습니다.'})


@app.route('/logout' , methods =['GET'])
def logout():
   session.pop('user_id')
   session.pop['sort']
   # session['logged_in'] = False
   return jsonify({'result' : 'success'})

@app.route('/registerInfo' , methods = ['POST'])
def registerInfo():
   user_id  = request.form['user_id']
   my_info  = request.form['my_info']
   name  = request.form['name']
   db.info.insert_one({'user_id' : user_id ,'name' : name , 'info' : my_info})
   return jsonify({'result' : 'success'})


@app.route('/myProfile/<user_id>')
def myProfile(user_id):
   user_info = db.user.find_one({'user_id' : user_id })
   my_info = list(db.info.find({'user_id' : user_info['user_id']}))
   sympathyList = list(db.sympathy.find({'user_id' : user_info['user_id']}))
   print(len(sympathyList))
   return render_template('myprofile.html' ,user_info = user_info , my_info = my_info , sympathyCnt = len(sympathyList))

@app.route('/yourProfile/<user_id>')
def yourProfile(user_id):
   user_info = db.user.find_one({'user_id' : user_id })
   common_content = list(db.info.find({'user_id' : user_info['user_id']}))
   return render_template('yourprofile.html' , common_content = common_content , user_name = user_info['name'] , user_id = user_info['user_id'])


@app.route('/deleteInfo', methods=['POST'])
def deleteInfo():
   pk = request.form['pk']
   db.sympathy.delete_many({'id' : pk})
   db.info.delete_one({'_id': ObjectId(pk)})
   return jsonify({'result' : 'success'})

@app.route('/sympathy' ,  methods=['POST'])
def clickSympathy() :
   user_id = request.form['user_id'];
   sympathy_person = request.form['sympathy_person'];
   sympathy_id = request.form['sympathy_id'];
   comment = request.form['info'];
   pk = request.form['pk'];
   # print("1111",len(comment))
   sympathy_value = db.sympathy.find_one({'id' :pk , 'sympathy_id' : sympathy_id })
   if sympathy_value == None :
      db.sympathy.insert_one({'id' : pk , 'user_id' : user_id , 'info' : comment ,'sympathy_id' : sympathy_id , 'sympathy_person' : sympathy_person});
      user = db.user.find_one({'user_id' : user_id},{'_id':False})
      print("ddd",user['sympathyCount'])
      db.user.update_one({'user_id' : user_id},{'$set' : {'sympathyCount' :user['sympathyCount']+1}})
      return jsonify({'result' : 'success'})
   else :
      print("이미 공감 누름")
      db.sympathy.delete_one({'id' : pk , 'sympathy_id' : sympathy_id} )
      return jsonify({'result' : 'fail'})



#시간순 정렬
@app.route('/orderbytime' , methods=['GET'])
def orderbytime():
   session['sort'] = 1
   return jsonify({'result': 'success'})

@app.route('/callSympathy', methods=['POST'])
def callSympathy() :
   info_pk = request.form['info_pk']
   sympathy_people = list(db.sympathy.find({'id' : info_pk },{'_id':False}))
   return jsonify({'data' : sympathy_people})



if __name__ == '__main__':
   app.secret_key = 'super secret key'
   app.run('0.0.0.0',port=5000,debug=True)