from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from models import Device

import json

# Create your views here.
def index(request):
    return HttpResponse("Welcome")

#Handles devices sending their software lists
@csrf_exempt
def device(request, device_uid):

    if request.method == "POST":
        json_data = json.loads(request.body)
        device = Device.objects.get(uid=device_uid)
        device.os = json_data['meta']['os_name']
        device.nickname = json_data['meta']['nickname']
        device.uid = device_uid
        device.save()
        
        #Next, Munge the software list at json_data['software'] to find CPEs, etc.

    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"  
    response["Access-Control-Allow-Methods"] = "POST"
    response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "*"  
    return response

