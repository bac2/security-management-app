from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Welcome")

#Handles devices sending their software lists
def device(request, device_uid):
    return HttpResponse("Congrats " + device_uid)

