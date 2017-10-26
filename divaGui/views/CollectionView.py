from divaGui.viewImports import *

class CollectionView(View):
    def get(self, request, *args, **kwargs):
        url = diva+self.kwargs['url']
        result = requests.get(url)
        result = result.json()
        name = url.split("/")
        name = name[-1]
        images = []
        numberOfFiles = 0
        statusCode = ''
        statusMessage = ''
        percentage = ''
        print(result)
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
            if temp != "png" and temp != "jpeg" and temp != "jpg" and temp != "JPG" and temp != "JPEG" and temp !="PNG":
                isXML = True

        imgNames = []

        for element in result['files']:
            temp = element['file']['identifier']
            temp = temp.split("/")
            imgNames.append(temp[1])

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