from ast import If
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import jwt, json, hashlib
import datetime as dt
import gridfs

app = Flask(__name__)
client = MongoClient('localhost',27017)
db = client.week1

SECRET_KEY = 'threeeeee'

# @app.route('/home')
# def home():
#    return render_template('main.html')

@app.route('/')
def main():
   # if session['sort'] == 1:
   #    user_list = list(db.mystar.find({}, {'_id': False}).sort('time', -1))

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



#아이디 중복확인
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
   after_password = hashlib.sha256(before_password.encode('utf-8')).hexdigest()
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
   user = db.user.find_one({'user_id' : login_id, 'password': login_after_pw})
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
   return render_template('myprofile.html' ,user_info = user_info , my_info = my_info , sympathyCnt = len(sympathyList))

@app.route('/yourProfile/<user_id>')
def yourProfile(user_id):
   user_info = db.user.find_one({'user_id' : user_id })
   sympathyList = list(db.sympathy.find({'user_id' :user_info['user_id']}))
   common_content = list(db.info.find({'user_id' : user_info['user_id']}))
   return render_template('yourprofile.html' , common_content = common_content , user_name = user_info['name'] , user_id = user_info['user_id'], count = len(sympathyList))


@app.route('/deleteInfo', methods=['POST'])
def deleteInfo():
   pk = request.form['pk'] # 유저 글 고유 번호
   user_id = request.form['user_id'] # 마이 프로필 글 삭제하는 유저 아이디
   sympathyList = list(db.sympathy.find({'id' : pk}))
   print(len(sympathyList))
   user = db.user.find_one({'user_id' : user_id},{'_id':False})
   db.sympathy.delete_many({'id' : pk})
   db.user.update_one({'user_id' : user_id},{'$set' : {'sympathyCount' :user['sympathyCount']-len(sympathyList)}})
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
   user = db.user.find_one({'user_id' : user_id},{'_id':False})
   sympathy_value = db.sympathy.find_one({'id' :pk , 'sympathy_id' : sympathy_id })
   if sympathy_value == None :
      db.sympathy.insert_one({'id' : pk , 'user_id' : user_id , 'info' : comment ,'sympathy_id' : sympathy_id , 'sympathy_person' : sympathy_person});
      print("ddd",user['sympathyCount'])
      db.user.update_one({'user_id' : user_id},{'$set' : {'sympathyCount' :user['sympathyCount']+1}})
      return jsonify({'result' : 'success'})
   else :
      print("이미 공감 누름")
      db.sympathy.delete_one({'id' : pk , 'sympathy_id' : sympathy_id} )
      db.user.update_one({'user_id' : user_id},{'$set' : {'sympathyCount' :user['sympathyCount']-1}})
      return jsonify({'result' : 'fail'})



#시간순 정렬
@app.route('/orderbytime' , methods=['GET'])
def orderbytime():
   session['sort'] = 1
   # stars = list(db.mystar.find({}, {'_id': False}).sort('time', -1))
   return jsonify({'result': 'success'})

@app.route('/callSympathy', methods=['POST'])
def callSympathy() :
   info_pk = request.form['info_pk']
   sympathy_people = list(db.sympathy.find({'id' : info_pk },{'_id':False}))
   return jsonify({'data' : sympathy_people})

@app.route("/upload", methods=['POST'])
def upload():
	## file upload ##
    img = request.files['image']
    
    ## GridFs를 통해 파일을 분할하여 DB에 저장하게 된다
    fs = gridfs.GridFS(db)
    fs.put(img, filename = 'name')
    
    ## file find ##
    data = client.grid_file.fs.files.find_one({'filename':'name'})
    
    ## file download ##
    my_id = data['_id']
    outputdata = fs.get(my_id).read()
    output = open('./images/'+'back.jpeg', 'wb')
    output.write(outputdata)
    return jsonify({'msg':'저장에 성공했습니다.'})

@app.route('/callSympathyCount' , methods=['POST'])
def callSympathyCount() :
   user_id = request.form['user_id']
   sympathy_people = list(db.sympathy.find({'user_id' : user_id },{'_id':False}))
   print("flask 서버 확인 !!!", sympathy_people)
   print("flask 서버 확인 !!222!", len(sympathy_people))
   return jsonify({'data' : sympathy_people})


if __name__ == '__main__':
   app.secret_key = 'super secret key'
   app.run('0.0.0.0',port=5000,debug=True)