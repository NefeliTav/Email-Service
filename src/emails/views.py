from django.shortcuts import render, redirect
from accounts.models import Account
import jwt


def home_view(request):
    if request.method == "POST":
        pass
    else:
        if 'jwt' in request.session:
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
            return render(request, 'email.html', data)
        else:
            return redirect("/auth/login")
