from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import jwt,json

app = Flask(__name__)
client = MongoClient('localhost',27017)
db = client.week1


@app.route('/')
def main():
   user_list = list(db.user.find({}))
   if "user_id" in session :
      user_id = session['user_id']
      return render_template('main.html', session_id = user_id , login = True , users = user_list)


   return render_template('main.html' , login = False , users = user_list)




@app.route('/signUp',methods = ['POST'])
def add_user():
   before_password = request.form['user_pw']
   after_password = jwt.encode({'password' : before_password} , 'abcde' , algorithm = 'HS256')
   user_name  = request.form['user_name']
   user_id = request.form['user_id']
   new_user = {'user_id' : user_id , 'name' : user_name , 'password' : after_password}
   db.user.insert_one(new_user)
   return jsonify({'result' : 'success'})



@app.route('/login' , methods=['POST'])
def login() :
   login_id = request.form['login_id']
   login_pw = request.form['login_pw']
   user = db.user.find_one({'user_id' : login_id})
   if user :
      password = jwt.decode(user['password'] ,'abcde' , algorithms=['HS256'])['password'] 
      if login_pw == password :
         session['logged_in'] = True
         session['user_id'] = login_id
         session['user_name'] = user['name']
         return jsonify({'result' : 'success'})

   return jsonify({'result' :'fail'})


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
   user_id  = request.form['user_id'];
   my_info  = request.form['my_info'];
   name  = request.form['name'];
   db.info.insert_one({'user_id' : user_id ,'name' : name , 'info' : my_info})
   return jsonify({'result' : 'success'})

    
@app.route('/yourProfile/<user_id>')
def you(user_id):
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
   info = request.form['info'];
   pk = request.form['pk'];
   db.sympathy.insert_one({'id' : pk , 'user_id' : user_id , 'info' : info ,'sympathy_id' : sympathy_id , 'sympathy_person' : sympathy_person});
   return jsonify({'result' : 'success'})

@app.route('/callSympathy', methods=['POST'])
def callSympathy() :
   info_pk = request.form['info_pk']
   print("ddsda", info_pk);
   sympathy_people = list(db.sympathy.find({'id' : info_pk },{'_id':False}))
   print("sympathy !!!" , sympathy_people)
   return jsonify({'data' : sympathy_people})


if __name__ == '__main__':
   app.secret_key = "123"
   app.run('0.0.0.0',port=5000,debug=True)