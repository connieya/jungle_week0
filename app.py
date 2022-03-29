from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient  
from bson import ObjectId
import jwt

app = Flask(__name__)

@app.route('/')
def home():
   return 'This is Home!'

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)