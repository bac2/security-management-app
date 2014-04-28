from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from models import Device, DeviceUpdate, UpdateApplications
from forms import AddDeviceForm
from vuln_search import find_vulnerabilities

import json
import re
import string

# Create your views here.
def index(request):
    return render_to_response("dashboard.html")

def device_list(request):
    account_devices = Device.objects.filter(owner=request.user)
    return render_to_response("devices.html", {"safe_devices": account_devices})

def device(request, device_uid):
    try:
        device = Device.objects.get(uid=device_uid)
    except Device.DoesNotExist:
        return HttpResponse("Device does not exist", status=404)
    try:
        update  = DeviceUpdate.objects.filter(device=device).latest("date")
        software = UpdateApplications.objects.filter(update=update)
        vulnerabilities = find_vulnerabilities(software)
    except:
        vulnerabilities = None

    return render_to_response("device.html", {"device": device, "vulnerabilities": vulnerabilities})

#Handles devices sending their software lists
@csrf_exempt
def device_update(request, device_uid):

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
            version = software['versionString'].lower()
            publisher = software['publisher'].lower()

            #Remove version strings in the software name
            match = re.match("(.*?)[Vv \.]*(ersion\.)?(\d+\.\d*)", name)
            if match:
                if software['versionString'] == "null":
                    software['versionString'] = match.group(2)
                name = match.group(1)

            #Publisher like "Microsoft Corporation" will find "Microsoft"
            publisher = publisher.split(",")[0] #Removes ", Inc" etc.
            publisher_words = publisher.split(" ")

            #Attempt to grab things like "amd"
            if len(publisher_words) > 2: #Only 3 or more words
                acronym = ""
                for word in publisher_words:
                    if len(word) > 0:
                        acronym += word[0]
                publisher_words.append(acronym)

            #Remove publisher names at the start, if we can
            for word in publisher_words:
                #Try and compare
                if word in name:
                    publisher = word
                    replaced_name = name.replace(word, "").strip()
                    #Products with a single name, e.g. Evernote by Evernote
                    if replaced_name != "":
                        name = replaced_name


        #Add software to the database now

    response = HttpResponse(device_uid)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

@login_required
def add_device(request):
    render_dict = {}
    success = False
    if request.method == 'POST':
        form = AddDeviceForm(request.POST)
        if form.is_valid():
            dev = Device(uid= form.cleaned_data["uid"], owner=request.user, nickname= form.cleaned_data["nickname"])
            dev.save()
            success = True
            form = AddDeviceForm()
        render_dict['success'] = success
    else:
        form = AddDeviceForm()

    render_dict["form"] = form
    return render_to_response("add_device.html", render_dict, context_instance=RequestContext(request))
