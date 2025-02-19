from django.shortcuts import render,HttpResponse

from django.contrib import messages

# from .models import *


def index (request):
    return render(request,"master/index.html")
