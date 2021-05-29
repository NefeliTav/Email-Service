from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.hashers import make_password, check_password
from .models import Account
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime
import json
import re


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


@csrf_exempt
def login(request):
    if request.method == "POST":
        # read data from client
        data = json.loads(request.body)

        email = data["email"]
        password = data["password"]

        # authenticate
        errors = {}
        try:
            obj = Account.objects.get(email=email+'@email.com')
            if not check_password(password, obj.password):
                errors["password"] = "Wrong password"
        except:
            errors["email"] = "This email address doesn't exist"

        # return error messages
        if errors != {}:
            return JsonResponse({'errors': errors})

        print("Login successful")
        # start session
        request.session['email'] = email
        # valid data -> go to home page
        return JsonResponse(data)
    else:
        return render(request, "accounts/login.html", {})


@csrf_exempt
def signup(request):

    if request.method == "POST":

        # read data from client
        data = json.loads(request.body)

        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        date_of_birth = data["date_of_birth"]
        password = data["password"]
        confirm = data["confirm"]

        # check if data is valid
        errors = {}
        try:
            obj = Account.objects.get(email=email+'@email.com')
            if obj:
                errors["email"] = "This email address already exists"
        except:
            pass

        if not first_name.replace(" ", "").isalpha():
            errors["firstname"] = "Invalid first name"

        if not last_name.replace(" ", "").isalpha():
            errors["lastname"] = "Invalid last name"

        if not validate_email(email + '@email.com'):
            errors["email2"] = "Invalid email address"

        if not valid_password(password):
            # not pretty
            errors["password"] = "Invalid password.Requirements:Minimum 8 characters.The letters must be between [a-z].At least one letter should be of Upper Case [A-Z].At least 1 number or digit between [0-9].At least 1 character from [ _ or @ or $ ]."

        if password != confirm:
            errors["confirm"] = "Passwords are not matching"

        if to_days(date_of_birth) < 4745:  # (365*13), the user is a child
            errors["date_of_birth"] = "You are too young to have an email account!"

        if errors != {}:
            return JsonResponse({'errors': errors})

        # valid data -> create user
        try:
            user = Account.objects.create(first_name=first_name, last_name=last_name, email=email+'@email.com',
                                          date_of_birth=date_of_birth, password=make_password(password))  # hash password
            user.save()

            # user is in db
            print('User Created')
            # go to home page
            return JsonResponse(data)
        except:
            # if any problem occurs, try again
            return render(request, "accounts/signup.html", {})

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
