from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))  # current location of my folder

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')  # Creating database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This is modification Tracker by SQL Alchemy

db = SQLAlchemy(app)  # passing object to create database
ma = Marshmallow(app)  # passing object for serialization to create schema

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100), unique=True)

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

# User schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')

user_schema = UserSchema()
users_schema = UserSchema(many=True)  # for multiple users

# Adding User
@app.route('/user', methods=['POST'])
def adduser():
    name = request.json['name']
    contact = request.json['contact']
    new_user = User(name,contact)
    
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user)

#displaying User 
@app.route("/user",methods=["GET"])
def getuser():
    alluser = User.query.all() #default funtion in SQL Database 
    result = users_schema.dump(alluser)
    return jsonify(result)


#to Get User with Id 
@app.route("/user/<id>",methods=["GET"])
def getuserid(id):
    user = User.query.get(id) #default funtion in SQL Database 
    return user_schema.jsonify(user)


# update User with Id 
@app.route("/user/<id>",methods=["PUT"])
def updateuser(id):
    user = User.query.get(id) #default funtion in SQL Database
    name = request.json['name']
    contact = request.json['contact']
    user.name = name
    user.contact = contact 
    db.session.commit()
    return user_schema.jsonify(user)

# update User with Id 
@app.route("/user/<id>",methods=["DELETE"])
def deluser(id):
     user = User.query.get(id)
     db.session.delete(user)
     db.session.commit()
     return  user_schema.jsonify(user) 






if __name__ == '__main__':
    app.run(debug=True)
