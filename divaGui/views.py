import random
import requests
import json
import pprint

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django import forms
from django.http import HttpResponseRedirect

import base64

# Create your views here.

# function based view


def addcollection(request, url):
    name = ''
    if request.method == "POST":
        name = request.POST.get("ime")
        f = request.FILES['files']  # here you get the files needed
        files = request.FILES.getlist('files')
        num = len(files)
        i = 0
        for f in files:
            if i == 0:
                encoded = base64.b64encode(f.read())
            # print(encoded)
                ext = f.name.split(".")
                filename = ext[0]
                ext = ext[1]
                # print(ext)
                value = str(encoded)
                value = value[:-1]
                value = value.strip('b\'')

                data = {
                    "name": name,
                    "files": [
                        {
                            "type": "base64",
                            "value": value,
                            "name": filename,
                            "extension": ext
                        },
                    ]
                }
                data = json.dumps(data)
                headers = {'Content-type': 'application/json'}
                response = requests.post(
                    "http://divaservices.unifr.ch/api/v2/collections/", data=data, headers=headers)
            else:
                encoded = base64.b64encode(f.read())

            # print(encoded)

                ext = f.name.split(".")
                filename = ext[0]
                ext = ext[1]
                # print(ext)
                value = str(encoded)
                value = value[:-1]
                value = value.strip('b\'')

                data = {
                    "files": [
                        {
                            "type": "base64",
                            "value": value,
                            "name": filename,
                            "extension": ext
                        }
                    ]
                }

                data = json.dumps(data)
                headers = {'Content-type': 'application/json'}

                response = requests.put(
                    "http://divaservices.unifr.ch/api/v2/collections/" + name, data=data, headers=headers)

            i = i + 1
            if i == num:
                return HttpResponseRedirect("/collection/http://divaservices.unifr.ch/api/v2/collections/" + name)

    context = {

    }

    return render(request, 'add_collections.html', context)


def collection(request, url):
    result = requests.get(url)
    result = result.json()
    name = url.split("/")
    name = name[6]
    images = []
    numberOfFiles = 0
    statusCode = ''
    statusMessage = ''
    percentage = ''

    statusCode = result['statusCode']
    statusMessage = result['statusMessage']
    percentage = result['percentage']

    isXML = False

    for element in result['files']:
        temp = element['file']['url']
        images.append(temp)
        numberOfFiles = numberOfFiles + 1
        temp = temp.split(".")
        temp = temp[len(temp) - 1]
        if temp == "xml":
            isXML = True

    imgNames = []

    for element in result['files']:
        temp = element['file']['url']
        temp = temp.split("/")
        imgNames.append(temp[8])

    # KEEP IDENTATION!
    images = zip(images, imgNames)

    context = {
        "imgNames": imgNames,
        "isXML": isXML,
        "directLink": url,
        "name": name,
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "percentage": percentage,
        "numberOfFiles": numberOfFiles,
        "images": images,
        "result": result,
    }
    return render(request, "collection.html", context)

####################### VIEWS #############################


class ContactView(View):
    def get(self, request, *args, **kwargs):

        context = {}

        return render(request, "contact.html", context)


class DeleteCollectionView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "delete_collection.html", context)

    def post(self, request, *args, **kwargs):
        name = self.request.POST.get("name")
        # print(name)
        payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}
        response = requests.delete(
            "http://divaservices.unifr.ch/api/v2/collections/" + name, data=json.dumps(payload), headers=headers)
        context = {}
        return HttpResponseRedirect("/collections/")


class CollectionsView(View):
    def get(self, request, *args, **kwargs):
        name = self.request.GET.get('q')

        url = "http://divaservices.unifr.ch/api/v2/collections/"
        result = requests.get(url)
        result = result.json()
        collections = []
        # print the names and urls of each collection
        if not name:
            for element in result['collections']:
                collections.append(element)
        else:
            for element in result['collections']:
                if name in element['collection']['name']:
                    collections.append(element)
        context = {
            "collections": collections,
        }
        return render(request, "collections.html", context)


####################### TEMPLATE VIEWS #############################

class ContactTemplateView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ContactTemplateView,
                        self).get_context_data(*args, **kwargs)

        # OVDE JE TELO VIEW-A

        return context


######################## TRYOUTS ####################################


class TryoutsTemplateView(TemplateView):
    template_name = 'tryouts.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TryoutsTemplateView,
                        self).get_context_data(*args, **kwargs)

        # OVDE JE TELO VIEW-A

        return context
