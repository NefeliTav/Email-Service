from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.hashers import make_password
import datetime
import re
from .models import Account


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
    return render(request, "accounts/login.html", {})


def signup(request):
    if request.method == 'POST':

        # get data from frontend
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['tel']
        date_of_birth = request.POST['date']
        password = request.POST['psw']
        confirm = request.POST['psw2']

        # check if data is valid
        try:
            obj = Account.objects.get(email=email+'@email.com')
            if obj:
                message = {"message": "This email address already exists"}
                return render(request, "accounts/signup.html", message)
        except:
            pass
        if not first_name.replace(" ", "").isalpha():
            message = {"message": "Invalid name"}
            return render(request, "accounts/signup.html", message)
        if not last_name.replace(" ", "").isalpha():
            message = {"message": "Invalid surname"}
            return render(request, "accounts/signup.html", message)
        valid_email = validate_email(email + '@email.com')
        if not valid_email:
            message = {"message": "Invalid email address"}
            return render(request, "accounts/signup.html", message)
        if not valid_phone(phone):
            message = {"message": "Invalid phone number"}
            return render(request, "accounts/signup.html", message)
        if not valid_password(password):
            # not pretty
            message = {
                "message": "Invalid password.Requirements:Minimum 8 characters.The letters must be between [a-z].At least one letter should be of Upper Case [A-Z].At least 1 number or digit between [0-9].At least 1 character from [ _ or @ or $ ]."}
            return render(request, "accounts/signup.html", message)
        if password != confirm:
            message = {"message": "Passwords are not matching"}
            return render(request, "accounts/signup.html", message)
        if to_days(date_of_birth) < 4745:  # (365*13), the user is a child
            message = {"message": "You are too young to have an email account!"}
            return render(request, "accounts/signup.html", message)

        # valid data -> create user
        try:
            user = Account.objects.create(first_name=first_name, last_name=last_name, email=email+'@email.com',
                                          phone=phone, date_of_birth=date_of_birth, password=make_password(password))  # hash password
            user.save()
            # user is in db
            print('User Created')
            message = {"message": "success"}
        except:
            # if any problem occurs, try again
            return redirect('/signup')
        return render(request, "accounts/signup.html", message)
    else:
        return render(request, "accounts/signup.html", {})


def profile(request):
    return render(request, "accounts/profile.html", {})


def get_accounts(request):
    MAX_OBJECTS = 20
    accounts = Account.objects.all()[:MAX_OBJECTS]
    data = {"results": list(accounts.values(
        "first_name", "last_name", "email", "phone", "date_of_birth", "password"))}
    return JsonResponse(data)


def get_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    data = {"results": {
        "first_name": account.first_name,
        "last_name": account.last_name,
        "email": account.email,
        "phone": account.phone,
        "date_of_birth": account.date_of_birth,
        "password": account.password
    }}
    return JsonResponse(data)
