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

from links.links import *

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
                    diva, data=data, headers=headers)
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
                    diva + name, data=data, headers=headers)

            i = i + 1
            if i == num:
                return HttpResponseRedirect("/collection/"+name)

    context = {

    }

    return render(request, 'add_collections.html', context)


#def collection(request, url):
#    url = diva+url
#    print(url)
#    print("OVDEOVDEOVDEOVDEOVDEOVDEOVDEOVDEOVDEOVDEOVDEOVDE")
#    result = requests.get(url)
#    result = result.json()
#    name = url.split("/")
#    #name = name[6]
#    name = name[4]
#    images = []
#    numberOfFiles = 0
#    statusCode = ''
#    statusMessage = ''
#    percentage = ''
#    statusCode = result['statusCode']
#    statusMessage = result['statusMessage']
#    percentage = result['percentage']
#
#    isXML = False
#
#    for element in result['files']:
#    	temp = element['file']['url']
#    	images.append(temp)
#    	numberOfFiles = numberOfFiles + 1
#    	temp = temp.split(".")
#    	temp = temp[len(temp) - 1]
#    	if temp == "xml":
#    		isXML = True
#
#    imgNames = []
#
#    for element in result['files']:
#    	temp = element['file']['url']
#    	temp = temp.split("/")
#    	imgNames.append(temp[6])
#    	#imgNames.append(temp[8])
#
#    # KEEP IDENTATION!
#    images = zip(images, imgNames)
#
#    context = {
#	    "imgNames": imgNames,
#	    "isXML": isXML,
#	    "directLink": url,
#	    "name": name,
#	    "statusCode": statusCode,
#	    "statusMessage": statusMessage,
#	    "percentage": percentage,
#	    "numberOfFiles": numberOfFiles,
#	    "images": images,
#	    "result": result,
#	}
#    return render(request, "collection.html", context)

####################### VIEWS #############################

#######################################################################


class CollectionView(View):
    def get(self, request, *args, **kwargs):
        url = diva+self.kwargs['url']
        result = requests.get(url)
        result = result.json()
        name = url.split("/")
        #name = name[6]
        name = name[4]
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
        	imgNames.append(temp[6])
        	#imgNames.append(temp[8])

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

    def post(self, request, *args, **kwargs):
        filename = self.request.POST.get("filename")
        collection = self.request.POST.get("name")
        
        url = diva+collection+ '/'  + filename
        print(filename)
        print(url)
        payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}
        response = requests.delete(
            url, data=json.dumps(payload), headers=headers)
        print(response)
        response = requests.get(diva+collection)
        print(response)
        context = {}
        return HttpResponseRedirect("/collection/"+collection)



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
            diva + name, data=json.dumps(payload), headers=headers)
        context = {}
        return HttpResponseRedirect("/collections/")

class MethodsView(View):
    def get(self, request, *args, **kwargs):
        url = "http://divaservices.unifr.ch/api/v2/"

        result = requests.get(url)
        result = result.json()

        methods = []

        #print(result)
        for element in result:
            methods.append(element)

        context = {
            "methods": methods,
        }
        return render(request, "methods.html", context)

class MethodView(View):
    methodName = ""
    url = ""
    collectionName= ""

    def get(self, request, *args, **kwargs):
        url = self.kwargs['url']

        url = url.lower()
        url = url.replace(" ", "")

        MethodView.url = url


        showCollectionsForm = True
        showFilesForm = False

        #print(showFilesForm)

        response = requests.get(diva)
        response = response.json()
        collections = []

        for element in response['collections']:
                collections.append(element)

        #print(url)


        result = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
        result = result.json()

        MethodView.methodName = result['general']['name']

        detailsKeys = []
        detailsValues = []

        for element in result['general'].keys():
            detailsKeys.append(element)

        for element in result['general'].values():
            detailsValues.append(element)

        #print(detailsKeys)
        #print(detailsValues)

        context = {
            "detailsKeys": detailsKeys,
            "detailsValues": detailsValues,
            "methodName": result['general']['name'],
            "collections": collections,
            "showCollectionsForm": showCollectionsForm,
            "showFilesForm": showFilesForm,
            "url": url,
        }
        return render(request, "method.html", context)

    def post(self, request, *args, **kwargs):
        methodName = MethodView.methodName
        url = MethodView.url
        applicationFlag = self.request.POST.get("applicationFlag")
        filename = self.request.POST.getlist("sel2")
        collectionName = self.request.POST.get("sel1")

        if(collectionName):
            MethodView.collectionName = collectionName
        else:
            collectionName = MethodView.collectionName

        #print(collectionName)

        #print(applicationFlag)

        showCollectionsForm = False

        images = []
        imgNames = []
        
        if applicationFlag=="False":
            showFilesForm = True
            res = requests.get(diva+collectionName)
            res = res.json()

            
            numberOfFiles = 0
            statusCode = ''
            statusMessage = ''
            percentage = ''
            statusCode = res['statusCode']
            statusMessage = res['statusMessage']
            percentage = res['percentage']

            isXML = False

            for element in res['files']:
                temp = element['file']['url']
                images.append(temp)
                numberOfFiles = numberOfFiles + 1
                temp = temp.split(".")
                temp = temp[len(temp) - 1]
                if temp == "xml":
                    isXML = True

            

            for element in res['files']:
                temp = element['file']['url']
                temp = temp.split("/")
                imgNames.append(temp[6])
                #imgNames.append(temp[8])

            MethodView.imgNames = imgNames
        else:  #i have selected the collection and selected files from it
            showFilesForm = False
            imgNames = MethodView.imgNames
            print(filename)
            

        result = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
        result = result.json()

        #print("http://divaservices.unifr.ch/api/v2/"+url+"/1")

        detailsKeys = []
        detailsValues = []

        for element in result['general'].keys():
            detailsKeys.append(element)

        for element in result['general'].values():
            detailsValues.append(element)


        payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}
        #response = requests.delete(
        #    diva + name, data=json.dumps(payload), headers=headers)
        context = {
            "detailsKeys": detailsKeys,
            "detailsValues": detailsValues,
            "methodName": methodName,
            "showCollectionsForm": showCollectionsForm,
            "showFilesForm": showFilesForm,
            "collectionName": collectionName,
            "imgNames": imgNames,
        }
        return render(request, "method.html", context)

class CollectionsView(View):
    def get(self, request, *args, **kwargs):
        name = self.request.GET.get('q')

        url = diva
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
