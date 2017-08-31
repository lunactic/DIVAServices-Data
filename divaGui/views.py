import random
import requests
import json
import pprint

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django import forms

# Create your views here.

#function based view

def addcollection(request, url):

    if request.method=="POST":
        f = request.FILES['files'] # here you get the files needed
        print(f)
         

    context = {

    }

    return render(request,'add_collections.html',context)


def collection(request, url):

	result = requests.get(url)

	result = result.json()

	name = url.split("/")
	name = name[6]

	images = []

	numberOfFiles = 0;

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
		temp = temp[len(temp)-1]
		if temp == "xml":
			isXML = True

	imgNames = []

	
	for element in result['files']:
		temp = element['file']['url']
		temp = temp.split("/")
		imgNames.append(temp[8])


	#KEEP IDENTATION!	
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


class CollectionsView(View):
	def get(self, request, *args, **kwargs):

		name = self.request.GET.get('q')

		#print(name)

		#print(kwargs)

		#print(args)

		url = "http://divaservices.unifr.ch/api/v2/collections/"

		result = requests.get(url)

		result = result.json()

		collections = []
	    #print the names and urls of each collection
		if not name :

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
		context = super(ContactTemplateView, self).get_context_data(*args, **kwargs)

		#OVDE JE TELO VIEW-A

		return context


######################## TRYOUTS ####################################


class TryoutsTemplateView(TemplateView):
	template_name = 'tryouts.html'

	
	def get_context_data(self, *args, **kwargs):
		context = super(TryoutsTemplateView, self).get_context_data(*args, **kwargs)

		#OVDE JE TELO VIEW-A

		return context
