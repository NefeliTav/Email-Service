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

def home_view(request):
    if request.method == "POST":
        pass
    else:
        if 'jwt' in request.session:
            encoded_token = request.session['jwt']
            user_id = jwt.decode(encoded_token, 'SECRET',
                                 algorithms=['HS256'])['id']
            # print(user_id)
            account = Account.objects.get(id=user_id)

            # organize emails in categories

            is_receiver = Q(receiver=account.email)
            is_sender = Q(sender=account.email)
            is_spam = Q(isSpam=True)

            mailbox = list(Email.objects.filter(is_receiver & ~is_spam))  # inbox
            sent_emails = list(Email.objects.filter(is_sender))  # sent
            spam_list = list(Email.objects.filter(is_receiver & is_spam))  # spam

            # print(spam_list)

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
    account = Account.objects.get(id=user_id)
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

        if antispam.is_spam(content):   # check if email is spam
            isSpam = True
        else:
            isSpam = False

        print(isSpam)

        # valid data -> send email
        try:
            email = Email.objects.create(sender=data["email"],
                                         receiver=receiver,
                                         text=content,
                                         subject=subject,
                                         isSpam=isSpam)

            email.save()

            # email is in db
            print('Email Sent')

        except:
            # if any problem occurs, try again
            return render(request, "email.html", data)

        # valid data -> go to home page
        return HttpResponse(
            json.dumps(request.session['jwt']),
            status=200,
            content_type="application/json"
        )

    else:

        return render(request, 'email.html', data)
