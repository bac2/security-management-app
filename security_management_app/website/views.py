from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Q
from django.core import serializers
from models import Device, DeviceUpdate, UpdateApplications, Cpe, Reference
from models import Device, DeviceUpdate, UpdateApplications, Cpe, Reference, Application
from forms import AddDeviceForm
from vuln_search import find_vulnerabilities

#from vuln_search import find_vulnerabilities

import json
from fuzzywuzzy import fuzz
import re
import string
from datetime import datetime

# Create your views here.
def index(request):
    return render_to_response("dashboard.html")

@login_required
def device_list(request):
    account_devices = Device.objects.filter(owner=request.user)
    safe_devices = []
    vulnerable_devices = []
    no_data_devices = []
    vuln_dict = {}
    severities = {}
    devices = False
    if account_devices:
        max_cvss = 0
        devices = True
        for device in account_devices:
            try:
                update  = DeviceUpdate.objects.filter(device=device).latest("date")
                software = UpdateApplications.objects.filter(update=update)
                vulnerabilities = find_vulnerabilities(software)
                if vulnerabilities:
                    vulnerable_devices.append(device)
                    vuln_dict[device] = vulnerabilities
                    for vuln in vulnerabilities:
                        if vuln.score > max_cvss:
                            max_cvss = vuln.score
                    severities[device] = max_cvss
            except:
                no_data_devices.append(device)

    return render_to_response("devices.html", {"devices": devices, "safe_devices": safe_devices, "vulnerable_devices": vulnerable_devices, "no_data_devices": no_data_devices, "vulnerabilities": vulnerabilities, "severities": severities})

@login_required
def device(request, device_uid):
    try:
        device = Device.objects.get(uid=device_uid)
    except Device.DoesNotExist:
        return HttpResponse("Device does not exist", status=404)
    try:
        update  = DeviceUpdate.objects.filter(device=device).latest("date")
        software = Application.objects.filter(updateapplications__update=update)
        vulnerabilities = find_vulnerabilities(update)
        for vuln in vulnerabilities:
            try:
                references = Reference.objects.get(vulnerability=vuln)
            except:
                references = None
            vuln.references = references
    except StandardError,e:
        print e
        vulnerabilities = None

    return render_to_response("device.html", {"device": device, "vulnerabilities": vulnerabilities})

@login_required
def graph_data(request):
    account_devices = Device.objects.filter(owner=request.user)
    for device in account_devices:
        try:
            update  = DeviceUpdate.objects.filter(device=device).latest("date")
            software = UpdateApplications.objects.filter(update=update)
            vulnerabilities = find_vulnerabilities(software)
            if vulnerabilities:
                device.vulnerabilities = vulnerabilities
        except:
            pass
    jsondata = serializers.serialize('json', account_devices)
    return HttpReponse(jsondata,mimetype='application/json')

#Handles devices sending their software lists
@csrf_exempt
def device_update(request, device_uid):

    if request.method == "POST":
        safe = 0
        unsafe = 0
        similar = 0
        unique_apps = {}
        json_data = json.loads(request.body.decode("unicode_escape"))
        try:
            device = Device.objects.get(uid=device_uid)
        except Device.DoesNotExist:
            return HttpResponse("Device does not exist", status=404)

        #Next, Munge the software list at json_data['software'] to find CPEs, etc.
        for software in json_data['software']:
            name = unicode(software['name'].lower())
            version = unicode(software['versionString'].lower())
            publisher = unicode(software['publisher'].lower())

            #Remove version strings in the software name
            match = re.match("(.*?)[Vv \.]*(ersion\.)?(\d+(\.\d*)+)(.*)", name)
            if match:
                if version == "null" and match.group(3) is not None:
                    version = match.group(3)
                name = match.group(1)

            if version == "null":
                continue

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

            #Remove some brackets (Usually x64 stuff)
            brackets = re.search("(\(.*\))", name)
            if brackets:
                name = name.replace(brackets.group(1), "").strip()

            #Remove publisher names at the start, if we can
            for word in publisher_words:
                #Try and compare
                if word in name:
                    publisher = word
                    replaced_name = name.replace(word, "").strip()
                    #Products with a single name, e.g. Evernote by Evernote
                    if len(replaced_name) > 5: #Less than 3 characters
                        name = replaced_name

            if name == publisher + "t":
                name = publisher

            publisher = publisher.strip().replace(" ", "_")
            name = name.strip().replace(" ", "_")

            out = publisher +" - " + name + " - " + version

            try:
                #Try to do stuff
                unique_apps[out] = App(publisher, name, version, software["name"])
            except KeyError:
                unique_apps[out] = App(publisher, name, version, software["name"])

        for key in sorted(unique_apps.keys(), key=lambda x: unique_apps[x].publisher):
            app = unique_apps[key]
            out = key

            matched = False

            non_match = Cpe.objects.filter(Q(product=app.name), ~Q(product=app.name, version=app.version))
            matches = Cpe.objects.filter(product=app.name, version=app.version)
            if matches.count() > 0:
                matched = True
                out += " VULNERABLE"
                unsafe += 1
                app.cpe = matches[0]
            if non_match.count() > 0 and matches.count() == 0:
                matched = True
                out += " SAFE"
                safe += 1
                app.related_cpe = non_match[0]

            close = Cpe.objects.filter(vendor=app.publisher, product__contains=app.name)
            close_match = Cpe.objects.filter(vendor=app.publisher, product__contains=app.name, version=app.version)
            if close.count() > 0 and matches.count() == 0 and non_match.count() == 0:
                matched = True
                out +="SAFE"
                safe += 1
                app.related_cpe = close[0]
            if close_match.count() > 0 and close.count() == 0 and matches.count() == 0 and non_match.count() == 0:
                matched = True
                out += " VULNERABLE"
                unsafe += 1
                app.cpe = close_match[0]

            if not matched:
                prods = Cpe.objects.filter(version__contains=app.version)
                for prod in prods:
                    if prod.product.replace("_", " ") in app.title.lower():
                        matched = True
                        out += " SIMILAR-------------- " + prod.product
                        similar += 1
                        app.cpe = prod
                    else:
                        try:
                            dist = fuzz.token_set_ratio(prod.product.decode("unicode_escape"), app.title)
                        except UnicodeEncodeError:
                            dist = 0

                        if dist > 80:
                            matched = True
                            out += " SIMILAR" + "---------------" + prod.product
                            similar += 1

            if matched:
                print out




        print safe, "safe"
        print unsafe, "unsafe"
        print similar, "similar"
        print len(unique_apps), "total"

        #Add a new device update
        d = DeviceUpdate(date=datetime.now(), device=device)
        d.save()

        #For each app, find if it has been added for this device
        matched_apps = [ app for key,app in unique_apps.items() if app.cpe is not None]
        for app in matched_apps:
            #Attach to an application
            #This shouldnt exist
            newApp = Application(cpe=app.cpe)
            newApp.save()

            up = UpdateApplications(update=d, application=newApp)
            up.save()

        detected_apps = [ app for key,app in unique_apps.items() if app.related_cpe is not None]
        for app in detected_apps:
            #Make a new CPE from the related CPE
            cpe = Cpe(  
                        cpe=app.related_cpe.cpe + ":RELATED:" + app.version,
                        part=app.related_cpe.part,
                        vendor=app.related_cpe.vendor,
                        product=app.related_cpe.product,
                        version=app.version,
                        update=app.related_cpe.update,
                        edition=app.related_cpe.edition,
                        language=app.related_cpe.language,
                        sw_edition=app.related_cpe.sw_edition,
                        target_sw=app.related_cpe.target_sw,
                        target_hw=app.related_cpe.target_hw,
                        other=app.related_cpe.other,
                        title=app.related_cpe.title
                    )
            cpe.save()
            #Create a new application
            newApp = Application(cpe=cpe)
            newApp.save()

            upApp = UpdateApplications(update=d, application=newApp)
            upApp.save()


    response = HttpResponse(device_uid)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

class App:
    def __init__(self, vendor, name, version, title):
        self.name = name
        self.publisher = vendor
        self.version = version
        self.title = title
        self.cpe = None
        self.related_cpe = None


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
