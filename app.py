from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import jwt

app = Flask(__name__)
client = MongoClient('localhost',27017)
db = client.week1
@app.route('/')
def main():
   return render_template('main.html')

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
         session['loggied_in'] = True
         # cname = db.user.find_one({'user_id' , login_id})
         # session['membername'] = cname['username']
         session['user_id'] = user['user_id']
         session['user_name'] = user['name']
         return jsonify({'result' : 'success'})

   return jsonify({'result' :'fail'})

if __name__ == '__main__':
   app.secret_key = "123"
   app.run('0.0.0.0',port=5000,debug=True)