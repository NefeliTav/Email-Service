from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.hashers import make_password
from .models import Account
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
import datetime
import json
import re


def valid_phone(phone):
    expression = re.compile(
        "^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$")
    return expression.match(phone)


def valid_password(psw):
    '''
    Function taken from https://www.geeksforgeeks.org/python-program-check-validity-password/
    Minimum 8 characters.
    The letters must be between [a-z]
    At least one letters should be of Upper Case [A-Z]
    At least 1 number or digit between [0-9].
    At least 1 character from [ _ or @ or $ ].
    '''
    if (len(psw) < 8):
        return False
    elif not re.search("[a-z]", psw):
        return False
    elif not re.search("[A-Z]", psw):
        return False
    elif not re.search("[0-9]", psw):
        return False
    elif not re.search("[_@$]", psw):
        return False
    elif re.search("\s", psw):
        return False
    return True


def to_days(then):
    now = datetime.datetime.now()
    date_time_obj = datetime.datetime.strptime(then, '%Y-%m-%d').date()
    diff = (now.date() - date_time_obj)
    diff = str(diff).split(' ')
    return int(diff[0])


def login(request):
    if request.method == "POST":
        data = request.read()

        # get data from frontend and convert it to json
        data = data.decode('utf8').replace("'", '"')
        data = json.loads(data)
        data = json.dumps(data, indent=4, sort_keys=True)
        data = json.loads(data)

        email = data["email"]
        password = data["password"]

        # check if data is valid
        try:
            obj = Account.objects.get(email=email+'@email.com')
            if not obj:
                message = {"message": "Wrong email address."}
                # return render(request, "accounts/login.html", message)
                # try again
                return redirect('/login')
        except:
            pass

        # start session
        request.session['email'] = email
        # valid data -> go to home page
        # return render(request, "accounts/homepage.html", {"email":email})

    else:
        return render(request, "accounts/login.html", {})


def signup(request):

    if request.method == "POST":
        data = request.read()

        # get data from frontend and convert it to json
        data = data.decode('utf8').replace("'", '"')
        data = json.loads(data)
        data = json.dumps(data, indent=4, sort_keys=True)
        data = json.loads(data)

        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        phone = data["phone"]
        date_of_birth = data["date_of_birth"]
        password = data["password"]
        confirm = data["confirm"]

        # check if data is valid
        try:
            obj = Account.objects.get(email=email+'@email.com')
            if obj:
                message = {"message": "This email address already exists"}
                # return render(request, "accounts/signup.html", message)
                # try again
                return redirect('/signup')
        except:
            pass

        if not first_name.replace(" ", "").isalpha():
            message = {"message": "Invalid name"}
            # try again
            return redirect('/signup')

        if not last_name.replace(" ", "").isalpha():
            message = {"message": "Invalid surname"}
            # try again
            return redirect('/signup')

        valid_email = validate_email(email + '@email.com')
        if not valid_email:
            message = {"message": "Invalid email address"}
            # try again
            return redirect('/signup')

        if not valid_phone(phone):
            message = {"message": "Invalid phone number"}
            # try again
            return redirect('/signup')

        if not valid_password(password):
            # not pretty
            message = {
                "message": "Invalid password.Requirements:Minimum 8 characters.The letters must be between [a-z].At least one letter should be of Upper Case [A-Z].At least 1 number or digit between [0-9].At least 1 character from [ _ or @ or $ ]."}
            # try again
            return redirect('/signup')

        if password != confirm:
            message = {"message": "Passwords are not matching"}
            # try again
            return redirect('/signup')

        if to_days(date_of_birth) < 4745:  # (365*13), the user is a child
            message = {"message": "You are too young to have an email account!"}
            # try again
            return redirect('/signup')

        # valid data -> create user
        try:
            user = Account.objects.create(first_name=first_name, last_name=last_name, email=email+'@email.com',
                                          phone=phone, date_of_birth=date_of_birth, password=make_password(password))  # hash password
            user.save()
            # user is in db
            print('User Created')
            # go to home page
        except:

            # if any problem occurs, try again
            return redirect('/signup')

    else:
        return render(request, "accounts/signup.html", {})


def profile(request):
    return render(request, "accounts/profile.html", {})


def get_accounts(request):
    accounts = list(Account.objects.values())
    return JsonResponse(accounts, safe=False)


def get_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    data = {"id": account.id,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "email": account.email,
            "phone": account.phone,
            "date_of_birth": account.date_of_birth,
            "password": account.password
            }
    return JsonResponse(data)


def delete_account(request, pk):
    try:
        account = Account.objects.get(pk=pk)
        account.delete()
        return JsonResponse({"deleted": True}, safe=False)
    except:
        return JsonResponse({"error": "not a valid primary key"}, safe=False)


def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return HttpResponse("<strong>You are logged out.</strong>")
