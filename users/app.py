from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import jwt
import bcrypt
#from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# USERDB_HOST = "userdb:27017"
# #USERDB_HOST = "localhost:27117"
# USERDB_USERNAME = 'userdb_client'
# USERDB_PASSWORD = 'hiddenpassword'
USERDB_HOST = "userdb-0.userdb,userdb-1.userdb,userdb-2.userdb:27017"

def generate_password_hash(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    #return str(bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()))
    return plain_text_password

def check_password_hash(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    #return str(bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password))
    return plain_text_password == hashed_password

def get_user(user_id=None, email=None):
    client = MongoClient(USERDB_HOST)

    userdb = client['userdb']

    rule = {}
    if user_id is not None:
        rule['_id'] = ObjectId(user_id)
    if email is not None:
        rule['email'] = email

    try:
        response = userdb.mycoll.find(rule)
    except:
        raise
        return False

    return list(response)


@app.route("/createaccount", methods=["POST"])
def create_account():
    json = request.json
    client = MongoClient(USERDB_HOST)

    userdb = client['userdb']
    try:
        json['password'] = generate_password_hash(json['password'])
        user_id = userdb.mycoll.insert_one(json).inserted_id
    except:
        raise
        return jsonify(status='Fail')

    json['status'] = 'Success'
    json['user_id'] = str(user_id)
    del json['_id']
    return jsonify(json)


@app.route("/updatepassword", methods=["POST"])
def update_password():
    json = request.json
    client = MongoClient(USERDB_HOST)

    userdb = client['userdb']

    try:
        userdb.mycoll.update_one({'_id' : ObjectId(json['user_id'])},
                                {'$set' : {'password' : generate_password_hash(json['password'])}})
    except:
        raise
        return jsonify(status='Fail')

    return jsonify(status='Success')

@app.route("/getaccount", methods=["POST"])
def get_account():
    json = request.json

    user = get_user(json['user_id'], json['email'])

    if not user or len(user) == 0:
        return jsonify(status='Fail')

    user = user[0]
    return jsonify(status='Success',
                   user_id=str(user['_id']),
                   first_name=user['first_name'],
                   last_name=user['last_name'],
                   email=user['email'],
                   date_of_birth=user['date_of_birth'],
                   password=user['password'])


@app.route("/autenticate", methods=["POST"])
def autenticate():
    json = request.json

    user = get_user(email=json['email'])
    print(user)

    if user == False:
        return jsonify(status='Fail')

    if len(user) == 0:
        return jsonify(status='Wrong')

    user = user[0]
    if not check_password_hash(json['password'], user['password']):
        return jsonify(status='Wrong')

    user_id = str(user['_id'])
    return jsonify(status='Success',
                   token=jwt.encode({'id': user_id}, 'SECRET', algorithm='HS256')
    )



if __name__ == "__main__":
    app.run(host='0.0.0.0')
