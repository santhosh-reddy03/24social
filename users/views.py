from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate


# Create your views here.

# @login_required()
def home(request):
    return "hello"



def logout_view(request):
    logout(request)