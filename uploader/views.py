from django.shortcuts import render
from uploader.models import UploadForm,Upload
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import requests
import json
import base64
from links.links import *
# Create your views here.



def uploader(request, url):


    if request.method=="POST":
        files = request.FILES.getlist('sentFile') # here you get the files needed

        num = len(files)

        i=0

        for f in files:
        	#print(f.name)
        	#print(f.read())

        	encoded = base64.b64encode(f.read())

        	#print(encoded)

        	ext = f.name.split(".")
        	filename = ext[0]
        	ext = ext[1]
        	#print(ext)

        	value = str(encoded)
        	value = value[:-1]
        	value = value.strip('b\'')

        	#print(value)

	        data = {
	            "files":[
	            {
	                "type":"base64",
	                "value": value,
	                "name": filename,
	                "extension": ext
	            }
	            ]
	        }

	        data = json.dumps(data)
	        headers = {'Content-type': 'application/json'}

	        #print(data)
	        response=requests.put(diva+url, data=data, headers=headers)



	        res = response.json()


	        if 'errorType' in res:
	            if res['errorType']=='ExistingFileError':
	                print('AHA! FILE EXISTS ALREADY!')


	        i = i+1

	        if i==num:
	            return HttpResponseRedirect("/collection/" + url)

	        #return HttpResponseRedirect("/collection/" + url.strip("/"))



    images=Upload.objects.all()

    context = {
    	'name': url,
    	'images': images,
    }

    return render(request,'uploader.html',context)
