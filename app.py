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
   after_password = jwt.encode({'password' , before_password} , 'abcde' , algorithm = 'HS256')
   user_name  = request.form['user_name']
   user_id = request.form['user_id']
   print("@@@@@" ,before_password,user_name,user_id)
   new_user = {'user_id' : user_id , 'name' : user_name , 'password' : after_password}
   db.user.insert_one(new_user)
   return jsonify({'result' : 'success'}) 


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)