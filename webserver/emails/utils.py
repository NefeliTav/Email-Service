from django.conf import settings
from .models import Email
from pymongo import MongoClient
import requests

def is_spam(subject=None, content=None):
    request = { 'subject' : subject, 'content' : content }

    response = requests.post(settings.ANTISPAM_CHECK_URL, json=request)
    json = response.json()

    return json['is_spam']

def save_email(sender=None, receiver=None, content=None, subject=None, is_spam=None):
    client = MongoClient(settings.USERDB_HOST)

    emaildb = client['emaildb']
    emaildb.mycoll.insert_one({'sender' : sender,
                               'receiver' : receiver,
                               'content' : content,
                               'subject' : subject,
                               'is_spam' : is_spam,
                               })

def get_emails(sender=None, receiver=None, is_spam=None):
    client = MongoClient(settings.USERDB_HOST)

    emaildb = client['emaildb']

    rule = {}
    if sender is not None:
        rule['sender'] = sender
    if receiver is not None:
        rule['receiver'] = receiver
    if is_spam is not None:
        rule['is_spam'] = is_spam

    response = emaildb.mycoll.find(rule)

    emails = []
    for e in response:
        emails.append(Email(sender=e['sender'],
                            receiver=e['receiver'],
                            text=e['content'],
                            subject=e['subject'],
                            isSpam=e['is_spam']))

    return emails
