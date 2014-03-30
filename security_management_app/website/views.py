from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse("Welcome")

#Handles devices sending their software lists
@csrf_exempt
def device(request, device_uid):
    response = HttpResponse("Hello " + device_uid)
    response["Access-Control-Allow-Origin"] = "*"  
    response["Access-Control-Allow-Methods"] = "POST"
    response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "*"  
    return response

