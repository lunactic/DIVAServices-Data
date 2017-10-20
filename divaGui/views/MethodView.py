from divaGui.viewImports import *

class MethodView(View):
    methodName = ""
    url = ""
    collectionName= ""
    filenames = ""
    isXML = False
    imagesUrls = []
    images = []
    selects = []
    numbers = []
    highlighters = []
    inputParams = ""

    def get(self, request, *args, **kwargs):
        url = self.kwargs['url']

        url = url.lower()
        url = url.replace(" ", "")

        MethodView.url = url

        #print(url)

        showCollectionsForm = True
        showFilesForm = False

        #print(showFilesForm)

        response = requests.get(diva)
        response = response.json()
        collections = []

        for element in response['collections']:
                collections.append(element)


        result = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
        result = result.json()

        MethodView.methodName = result['general']['name']

        detailsKeys = []
        detailsValues = []

        for element in result['general'].keys():
            detailsKeys.append(element)

        for element in result['general'].values():
            detailsValues.append(element)

        details = zip(detailsKeys, detailsValues)

        

        context = {
            "details": details,
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
        filenames = self.request.POST.getlist("sel2")
        collectionName = self.request.POST.get("sel1")
        finalStep = self.request.POST.get("finalStep")


       
        MethodView.images = MethodView.images

        if(collectionName):
            MethodView.collectionName = collectionName
        else:
            collectionName = MethodView.collectionName

        showCollectionsForm = False
        showFilesForm = False


        imagesUrls = []
        imgNames = []
        selects = []
        numbers = []
        highlighters = []

        MethodView.isXML = False

        reqestMethodJson = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
        inputParams = reqestMethodJson.json()
        MethodView.inputParams = inputParams
        
        if applicationFlag=="False" and finalStep!="True":
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

            for element in res['files']:
                temp = element['file']['identifier']
                temp = temp.split("/")
                imgNames.append(temp[1])

            MethodView.imgNames = imgNames
            #print('prvipost')

        if applicationFlag=="True" and finalStep!="True":  #i have selected the collection and selected files from it
            showFilesForm = False
            MethodView.filenames = filenames
            #print(filenames)

            res = requests.get(diva+collectionName)
            res = res.json()

            for element in res['files']:
                temp = element['file']['url']
                temp = temp.split("/")
                if temp[6] in filenames:
                    imagesUrls.append(element['file']['url'])
                    temp = temp[6].split(".")
                    temp = temp[len(temp) - 1]
                    if temp != "png" and temp != "jpeg" and temp != "jpg" and temp != "JPG" and temp != "JPEG" and temp !="PNG":
                        MethodView.isXML = True

            MethodView.imagesUrls = imagesUrls
            MethodView.images = zip(imagesUrls, filenames)

            reqestMethodJson = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
            inputParams = reqestMethodJson.json()

            for element in inputParams['input']:
                if 'select' in element:
                    selects.append(element)
                if 'number' in element:
                    numbers.append(element)
                if 'highlighter' in element:
                    highlighters.append(element)
                    print(highlighters[0])
            #print('drugipost')

            MethodView.inputParams = inputParams
            MethodView.selects = selects
            MethodView.numbers = numbers
            MethodView.highlighters = highlighters

        if finalStep=="True": #apply method to selected images with set up input parameters
            showFilesForm = False
            showCollectionsForm = False

            MethodView.images = zip(MethodView.imagesUrls, MethodView.filenames)

            

        result = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
        result = result.json()

        #print("http://divaservices.unifr.ch/api/v2/"+url+"/1")

        detailsKeys = []
        detailsValues = []

        for element in result['general'].keys():
            detailsKeys.append(element)

        for element in result['general'].values():
            detailsValues.append(element)


        details = zip(detailsKeys, detailsValues)

        payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}
        #response = requests.delete(
        #    diva + name, data=json.dumps(payload), headers=headers)
        context = {
            "details": details,
            "methodName": methodName,
            "showCollectionsForm": showCollectionsForm,
            "showFilesForm": showFilesForm,
            "collectionName": collectionName,
            "imgNames": MethodView.imgNames,
            "images": MethodView.images,
            "isXML": MethodView.isXML,
            "url": url,
            "inputParams": MethodView.inputParams['input'],
            "selects": MethodView.selects,
            "numbers": MethodView.numbers,
            "highlighters": MethodView.highlighters,
            "finalStep": finalStep,
        }
        return render(request, "method.html", context)