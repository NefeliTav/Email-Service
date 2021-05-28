from django.http.response import HttpResponse
import rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render


def home_view(request):
    return render(request, 'index.html', {})
