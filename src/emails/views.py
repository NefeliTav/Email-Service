from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.hashers import make_password, check_password
from .models import Email
from accounts.models import Account
from validate_email import validate_email
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import date
import time
import json
import jwt
import re

import smtplib
from email.message import EmailMessage
import antispam

import emails.utils as emailutils
import accounts.utils as accountutils

def home_view(request):
    if request.method == "POST":
        pass
    else:
        if 'jwt' in request.session:
            encoded_token = request.session['jwt']
            user_id = jwt.decode(encoded_token, 'SECRET',
                                 algorithms=['HS256'])['id']
            # print(user_id)
            account = accountutils.get_account(user_id=user_id)

            # organize emails in categories

            mailbox = emailutils.get_emails(
                    receiver=account.email, is_spam=False)
            sent_emails = emailutils.get_emails(
                    sender=account.email)
            spam_list = emailutils.get_emails(
                    receiver=account.email, is_spam=True)

            # pass to frontend
            data = {"id": account.id,
                    "first_name": account.first_name,
                    "last_name": account.last_name,
                    "email": account.email,
                    "date_of_birth": str(account.date_of_birth),
                    "mailbox": mailbox,
                    "spam_list": spam_list,
                    "sent_emails": sent_emails
                    }
            return render(request, 'email.html', data)
        else:
            return redirect("/auth/login")

@csrf_exempt
def send(request):

    encoded_token = request.session['jwt']
    user_id = jwt.decode(encoded_token, 'SECRET',
                         algorithms=['HS256'])['id']
    account = accountutils.get_account(user_id=user_id)
    data = {"id": account.id,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "email": account.email,
            "date_of_birth": str(account.date_of_birth)
            }

    if request.method == "POST":

        # read data from client
        info = json.loads(request.body)

        receiver = info["receiver"]
        subject = info["subject"]
        content = info["content"]

        errors = {}
        if not validate_email(receiver):
            errors["receiver"] = "Invalid email address"

        # return error messages
        if errors != {}:
            return JsonResponse({'errors': errors})

        # check if email is spam
        try:
            is_spam = emailutils.is_spam(subject=subject,
                                         content=content)
        except:
            print('Skip spam check')
            is_spam = True

        # valid data -> send email
        try:
            emailutils.save_email(sender=data["email"],
                                  receiver=receiver,
                                  content=content,
                                  subject=subject,
                                  is_spam=is_spam)

            # email is in db
            print('Email Sent')

        except:
            # if any problem occurs, try again
            print('Email is not saved in DB')
            return render(request, "email.html", data)

        # valid data -> go to home page
        return HttpResponse(
            json.dumps(request.session['jwt']),
            status=200,
            content_type="application/json"
        )

    else:

        return render(request, 'email.html', data)
