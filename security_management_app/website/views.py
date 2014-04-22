from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from models import Device
from forms import AddDeviceForm

import json
import re

from django.shortcuts import *


# Create your views here.
def index(request):
    return render_to_response("dashboard.html")

#Handles devices sending their software lists
@csrf_exempt
def device(request, device_uid):

    if request.method == "POST":
        json_data = json.loads(request.body)
        try:
            device = Device.objects.get(uid=device_uid)
        except Device.DoesNotExist:
            return HttpResponse("Device does not exist", status=404)
        device.os = json_data['meta']['os_name']
        device.nickname = json_data['meta']['nickname']
        device.uid = device_uid
        device.save()

        #Next, Munge the software list at json_data['software'] to find CPEs, etc.
        for software in json_data['software']:
            name = software['name'].lower()

            match = re.match("(.*?)[Vv ]*(\d+\.\d*)", name)
            if match:
                if software['versionString'] == "null":
                    software['versionString'] = match.group(2)
                name = match.group(1)

        #name and software['versionString'] should be roughly correct.
        #I can't remove the potential "Microsoft"/publishers at the start though

    response = HttpResponse(device_uid)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def add_device(request):
    render_dict = {}
    if request.method == 'POST':
        success = False
        form = AddDeviceForm(request.POST)
        if form.is_valid():
            dev = Device(uid= form.cleaned_data["uid"], user=request.user)
            uid= form.cleaned_data["uid"]
            dev.user = request.user
            render_dict['success'] = success

    else:
        form = AddDeviceForm() # An unbound form

    return render_to_response("add_device.html", render_dict, context_instance=RequestContext(request))
