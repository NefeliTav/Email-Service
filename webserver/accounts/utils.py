from bson import ObjectId
from django.conf import settings
from .models import Account
import requests


def get_account(user_id=None, email=None):

    request = { 'user_id' : user_id, 'email' : email }
    response = requests.post(f'{settings.USERS_URL}/getaccount', json=request)
    json = response.json()

    if json['status'] == 'Fail':
        raise Exception('Password update failed!')

    return Account(user_id=json['user_id'],
                   first_name=json['first_name'],
                   last_name=json['last_name'],
                   email=json['email'],
                   date_of_birth=json['date_of_birth'],
                   password=json['password'])


def create_account(first_name=None, last_name=None, email=None,
        date_of_birth=None, password=None):

    request = { 'first_name' : first_name,
                'last_name' : last_name,
                'email' : email,
                'date_of_birth' : date_of_birth,
                'password' : password,
                }

    response = requests.post(f'{settings.USERS_URL}/createaccount', json=request)
    json = response.json()

    if json['status'] == 'Fail':
        raise Exception('Create account failed')

    return Account(user_id=json['user_id'],
                   first_name=json['first_name'],
                   last_name=json['last_name'],
                   email=json['email'],
                   date_of_birth=json['date_of_birth'],
                   password=json['password'])


def update_password(user_id=None, password=None):
    request = { 'user_id' : user_id, 'password' : password }
    response = requests.post(f'{settings.USERS_URL}/signup', json=request)
    json = response.json()

    if json['status'] == 'Fail':
        raise Exception('Password update failed!')


def autenticate(email=None, password=None):
    request = { 'email' : email, 'password' : password }

    response = requests.post(f'{settings.USERS_URL}/autenticate', json=request)
    print(response)
    json = response.json()

    if json['status'] == 'Fail':
        raise Exception('Autenticating failed!')

    if json['status'] == 'Wrong':
        return None

    return json['token']
