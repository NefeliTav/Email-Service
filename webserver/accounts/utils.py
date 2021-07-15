from bson import ObjectId
from django.conf import settings
from .models import Account
from pymongo import MongoClient

def get_account(user_id=None, email=None):
    client = MongoClient(settings.USERDB_HOST,
                         username=settings.USERDB_USERNAME,
                         password=settings.USERDB_PASSWORD)

    userdb = client['userdb']

    rule = {}
    if user_id is not None:
        rule['_id'] = ObjectId(user_id)
    if email is not None:
        rule['email'] = email

    response = userdb.mycoll.find(rule)
    user = response[0]

    return Account(user_id=str(user['_id']),
                   first_name=user['first_name'],
                   last_name=user['last_name'],
                   email=user['email'],
                   date_of_birth=user['date_of_birth'],
                   password=user['password'])

def create_account(first_name=None, last_name=None, email=None,
        date_of_birth=None, password=None):
    client = MongoClient(settings.USERDB_HOST,
                         username=settings.USERDB_USERNAME,
                         password=settings.USERDB_PASSWORD)

    userdb = client['userdb']
    user_id = userdb.mycoll.insert_one({'first_name' : first_name,
                                        'last_name' : last_name,
                                        'email' : email,
                                        'date_of_birth' : date_of_birth,
                                        'password' : password
                                        }).inserted_id

    return Account(user_id=id,
                   first_name=first_name,
                   last_name=last_name,
                   email=email,
                   date_of_birth=date_of_birth,
                   password=password)

def update_password(user_id=None, password=None):
    client = MongoClient(settings.USERDB_HOST,
                         username=settings.USERDB_USERNAME,
                         password=settings.USERDB_PASSWORD)

    userdb = client['userdb']
    userdb.mycoll.update_one({'_id' : ObjectId(user_id)},
                            {'$set' : {'password' : password}})
