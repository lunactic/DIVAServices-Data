from django.shortcuts import render
from uploader.models import UploadForm,Upload
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import requests
import json
import base64
# Create your views here.



def uploader(request, url):

    if request.method=="POST":
        f = request.FILES['sentFile'] # here you get the files needed
        

        print (f.name)

        encoded = base64.b64encode(f.read())

        #print(encoded)

        ext = f.name.split(".")
        filename = ext[0]
        ext = ext[1]
        print(ext)

        data = {
            "files":[
            {
                "type":"base64",
                "value": str(encoded),
                "name": filename,
                "extension": ext
            }
            ]
        }

        data = json.dumps(data)
        headers = {'Content-type': 'application/json'}

        #print(data)
        print(requests.put("http://divaservices.unifr.ch/api/v2/collections/"+url, data=data, headers=headers))

        # print(response)

        #return HttpResponseRedirect("/uploader/"+url)
        return HttpResponseRedirect("/collection/http://divaservices.unifr.ch/api/v2/collections/"+url)

                

    images=Upload.objects.all()

    context = {
    	'name': url,
    	'images': images,
    }

    return render(request,'uploader.html',context)