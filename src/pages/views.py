from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def login_view(request, *args, **kwargs):
    return render(request, "index.html", {})
