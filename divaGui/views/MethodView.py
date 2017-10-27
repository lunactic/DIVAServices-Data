from divaGui.viewImports import *

class MethodView(View):
    methodName = ""
    url = ""
    collectionName= ""
    filenames = []
    isXML = False
    imagesUrls = []
    images = []
    selects = []
    numbers = []
    highlighters = []
    inputParams = ""
    selectedSelects = []
    selectedNumbers = []
    selectedHighlighters = []
    responseToMethodApplication = json.dumps({})
    resultingImages = []
    imageUrls = []
    linksToResultingJson = []
    resultingImagesZip = []

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

            MethodView.imagesUrls = []
            for element in res['files']:
                temp = element['file']['url']
                temp = temp.split("/")
                if temp[-1] in filenames:
                    MethodView.imagesUrls.append(element['file']['url'])
                    temp = temp[-1].split(".")
                    temp = temp[len(temp) - 1]
                    if temp != "png" and temp != "jpeg" and temp != "jpg" and temp != "JPG" and temp != "JPEG" and temp !="PNG":
                        MethodView.isXML = True

            print("step before final: ")
            MethodView.filenames = filenames

            MethodView.images = zip(MethodView.imagesUrls, filenames)

            reqestMethodJson = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
            inputParams = reqestMethodJson.json()

            
            for element in inputParams['input']:
                if 'select' in element:
                    selects.append(element)
                if 'number' in element:
                    numbers.append(element)
                if 'highlighter' in element:
                    highlighters.append(element)
                    #print(highlighters[0])

            #print('drugipost')
            MethodView.inputParams = inputParams
            MethodView.selects = selects
            MethodView.numbers = numbers
            MethodView.highlighters = highlighters

        
        if finalStep=="True": #apply method to selected images with set up input parameters and save images to a collection
            showFilesForm = False
            showCollectionsForm = False

            MethodView.selectedSelects = []
            MethodView.selectedNumbers = []
            MethodView.selectedHighlighters = []
            MethodView.resultingImages = []

            #YOU CAN ITERATE ONLY ONCE THROUGH A ZIP!
            MethodView.images = zip(MethodView.imagesUrls, MethodView.filenames)

            #print("---Selected Selects---")
            index = 0 
            for element in MethodView.selects:
                temp = self.request.POST.get("select"+str(index))
                MethodView.selectedSelects.append(temp)
                #print(MethodView.selectedSelects[index])
                index = index + 1

            #print("---Selected Numbers---")
            index = 0 
            for element in MethodView.numbers:
                temp = self.request.POST.get("myRange"+str(index))
                MethodView.selectedNumbers.append(temp)
                #print(MethodView.selectedNumbers[index])
                index = index + 1

            #print("---Selected Highlighters---")
            index = 0
            for element in MethodView.highlighters:
                temp = self.request.POST.get("highlighter"+str(index))
                MethodView.selectedHighlighters.append(temp)
                #print(MethodView.selectedHighlighters[index])
                index = index + 1

            #now we finally have the parameter values and the images as well as the method name
            #and we below implement the actual method calls to the server in order to get back our resulting images           

            data = {
                "parameters":{},
                "data": [{}],
            }

            index = 0
            for element in MethodView.selects:
                data["parameters"][element["select"]["name"]] = str(MethodView.selectedSelects[index])

                index = index + 1

            index = 0
            for element in MethodView.numbers:
                data["parameters"][element["number"]["name"]] = str(MethodView.selectedNumbers[index])

                index = index + 1

            #TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE TO BE DONE

            #create input in case of highlighter

            #check if files are visualizable, otherwise just give links to results

            #create linking to result of each file individually rather than the whole group of them - check

            #create multiple selects for multiple input

            #enable collection creation from resulting files

            MethodView.linksToResultingJson = []
            
            for element in MethodView.imagesUrls:

                tempName = element.split('/')
                tempName = tempName[-1]

                data["data"][0] = {
                    "inputImage": collectionName + "/" + tempName,
                }

                dataSend = json.dumps(data)
                headers = {'Content-type': 'application/json'}
                responseToMethodApplication = requests.post("http://divaservices.unifr.ch/api/v2/"+url+"/1", data=dataSend, headers=headers)
                responseToMethodApplication = responseToMethodApplication.json()
                MethodView.responseToMethodApplication = responseToMethodApplication
                print("")
                print("Response of method application call:")
                print("")
                print(responseToMethodApplication)
                print("")
                if 'status' in responseToMethodApplication:
                    
                    resultingOutput = requests.get(responseToMethodApplication["results"][0]["resultLink"])
                    resultingOutput = resultingOutput.json()
                    #print("")
                    #print(resultingOutput)
                    #print("")

                    while (resultingOutput['status'] == 'planned'):
                        print('waiting on server..')
                        resultingOutput = requests.get(responseToMethodApplication["results"][0]["resultLink"])
                        resultingOutput = resultingOutput.json()

                    print(resultingOutput)

                    MethodView.linksToResultingJson.append(resultingOutput['resultLink'])

                    for element in resultingOutput['output']:
                        if element['file']['options']['visualization'] == True:
                            MethodView.resultingImages.append(element['file']['url'])
                        else :
                            if element['file']['options']['type'] != "logfile":
                                MethodView.resultingImages.append(element['file']['url'])

                    MethodView.resultingImagesZip = zip(MethodView.resultingImages,MethodView.linksToResultingJson)

                else: 
                    if 'errorType' in responseToMethodApplication:

                        print("")
                        print("ERROR BRANCH LINE 298 IN METHODVIEW.PY - SOMETHING IS BAD IN THE SENDING REQUEST (FILE NUMBER ETC..)")
                        print("")
                        print(responseToMethodApplication)
                        print("")

                        MethodView.linksToResultingJson.append(responseToMethodApplication['message'])
                        MethodView.resultingImages.append(responseToMethodApplication['message'])

            #print(MethodView.resultingImages)

        #print("http://divaservices.unifr.ch/api/v2/"+url+"/1")

        result = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
        result = result.json()

        detailsKeys = []
        detailsValues = []

        for element in result['general'].keys():
            detailsKeys.append(element)

        for element in result['general'].values():
            detailsValues.append(element)

        details = zip(detailsKeys, detailsValues)

        payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}

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
            "selectedNumbers": MethodView.selectedNumbers,
            "selectedHighlighters": MethodView.selectedHighlighters,
            "selectedSelects": MethodView.selectedSelects,
            "responseToMethodApplication": MethodView.responseToMethodApplication,
            "resultingImages": MethodView.resultingImages,
            "imageUrls": MethodView.imageUrls,
            "linksToResultingJson": MethodView.linksToResultingJson,
            "resultingImagesZip": MethodView.resultingImagesZip,
        }
        return render(request, "method.html", context)