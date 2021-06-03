from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.hashers import make_password, check_password
from .models import Account
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime
import json
import jwt
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
            user = Account.objects.get(email=email+'@email.com')
            if not check_password(password, user.password):
                errors["password"] = "Wrong password"
        except:
            errors["email"] = "This email address doesn't exist"

        # return error messages
        if errors != {}:
            return JsonResponse({'errors': errors})

        encoded_token = jwt.encode(
            {'id': user.id}, 'SECRET', algorithm='HS256')

        print("Login successful")
        # start session
        request.session['jwt'] = encoded_token

        # valid data -> go to home page
        return HttpResponse(
            json.dumps(encoded_token),
            status=200,
            content_type="application/json"
        )

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
            user = Account.objects.get(email=email+'@email.com')
            if user:
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
            errors["password"] = "Invalid password."

        if password != confirm:
            errors["confirm"] = "Passwords do not match"

        if to_days(date_of_birth) < 4745:  # (365*13), the user is a child
            errors["date_of_birth"] = "You are too young to have an email account!"

        if errors != {}:
            return JsonResponse({'errors': errors})

        # valid data -> create user
        try:
            user = Account.objects.create(first_name=first_name,
                                          last_name=last_name,
                                          email=email+'@email.com',
                                          date_of_birth=date_of_birth,
                                          password=make_password(password))  # hash password
            user.save()
            # user is in db
            print('User Created')

            encoded_token = jwt.encode(
                {'id': user.id}, 'SECRET', algorithm='HS256')
            # start session
            request.session['jwt'] = encoded_token

            # go to home page
            return HttpResponse(
                json.dumps(encoded_token),
                status=200,
                content_type="application/json"
            )

        except:
            # if any problem occurs, try again
            return render(request, "accounts/signup.html", {})

    else:
        return render(request, "accounts/signup.html", {})


@csrf_exempt
def profile(request):

    if "jwt" in request.session:

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

        if request.method == "PATCH":
            # read data from client
            data = json.loads(request.body)

            password = data["password"]
            confirm = data["confirm"]

            # check if data is valid
            errors = {}
            if not valid_password(password):
                errors["password"] = "Invalid password."

            if password != confirm:
                errors["confirm"] = "Passwords do not match"

            if errors != {}:
                return JsonResponse({'errors': errors})

            # valid data -> update user
            try:
                # update password
                Account.objects.filter(id=user_id).update(
                    password=make_password(password))  # hash password
            except:
                # if any problem occurs, try again
                return render(request, "accounts/profile.html", {"token": encoded_token})

            print('User Updated')

            # go to home page
            return JsonResponse({"user": "updated"})

        else:
            return render(request, "accounts/profile.html", data)
    else:
        return redirect("/auth/login")


def get_accounts(request):
    data = {"results": list(Account.objects.all().values("id",
                                                         "first_name", "last_name", "email", "date_of_birth"))}
    return JsonResponse(data)


def get_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    data = {"id": account.id,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "email": account.email,
            "date_of_birth": account.date_of_birth
            }
    return JsonResponse(data)


def delete_account(request, pk):
    try:
        account = Account.objects.get(pk=pk)
        account.delete()
        return JsonResponse({"deleted": True}, safe=False)
    except:
        return JsonResponse({"error": "no account with this id"}, safe=False)


@csrf_exempt
def logout(request):
    try:
        # print(request.session.session_key)
        del request.session["jwt"]
        request.session.flush()
    except:
        return JsonResponse({"logged out": "false"})
    return JsonResponse({"logged out": "true"})
