from divaGui.viewImports import *

from PIL import Image

from io import BytesIO

class MethodView(View):
    methodName = ""
    url = ""
    collectionName= ""
    filenames = []
    isXML = False
    imagesUrls = []
    imgNames = []
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
    detailsKeys = []
    detailsValues = []
    details = []
    resultingFileNames = []
    filesInputDetails = []
    foldersInputDetails = []
    filesInputDetailsName = []
    foldersInputDetailsName = []
    filesInputDetailsDescription = []
    foldersInputDetailsDescription = []
    fileCollectionNames = []
    folderCollectionNames = []

    colectionsFilesNames = []

    imageFileNames = []

    selectedInputJson = {}

    singleFileCollectionInput = True
    singleFolderCollectionInput = True
    folderInput = False
    fileInput = False

    highlightersExist = False
    multipleInput = False

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


        if(MethodView.methodName == ""):
            MethodView.methodName = result['general']['name']

        MethodView.detailsKeys = []
        for element in result['general'].keys():
            MethodView.detailsKeys.append(element)

        MethodView.detailsValues = []
        for element in result['general'].values():
            MethodView.detailsValues.append(element)

        MethodView.details = zip(MethodView.detailsKeys, MethodView.detailsValues)

        MethodView.singleFileCollectionInput = True
        MethodView.singleFolderCollectionInput = True
        MethodView.folderInput = False
        MethodView.highlightersExist = False
        MethodView.multipleInput = False

        MethodView.fileCollectionNames = []
        MethodView.folderCollectionNames = []
        MethodView.filesInputDetailsName = []
        MethodView.filesInputDetailsDescription = []
        MethodView.foldersInputDetailsName = []
        MethodView.foldersInputDetailsDescription = []

        for element in result['input']:
            if 'file' in element and element['file']['userdefined']==True:
                MethodView.filesInputDetailsName.append(element['file']['name'])
                MethodView.filesInputDetailsDescription.append(element['file']['description'])
                MethodView.filesInputDetails = zip(MethodView.filesInputDetailsName,MethodView.filesInputDetailsDescription)
                
                MethodView.fileInput = True

            if 'folder' in element and element['folder']['userdefined']==True:
                MethodView.foldersInputDetailsName.append(element['folder']['name'])
                MethodView.foldersInputDetailsDescription.append(element['folder']['description'])
                MethodView.foldersInputDetails = zip(MethodView.foldersInputDetailsName,MethodView.foldersInputDetailsDescription)

                MethodView.folderInput = True

        if len(MethodView.filesInputDetailsName) > 1 :
            MethodView.singleFileCollectionInput = False

        if len(MethodView.foldersInputDetailsName) > 1 :
            MethodView.singleFolderCollectionInput = False

        context = {
            "details": MethodView.details,
            "filesInputDetails": MethodView.filesInputDetails,
            "foldersInputDetails": MethodView.foldersInputDetails,
            "filesInputDetailsName": MethodView.filesInputDetailsName,
            "foldersInputDetailsName": MethodView.foldersInputDetailsName,
            "methodName": result['general']['name'],
            "collections": collections,
            "showCollectionsForm": showCollectionsForm,
            "showFilesForm": showFilesForm,
            "url": url,
        }
        return render(request, "method.html", context)

    def post(self, request, *args, **kwargs):
        url = MethodView.url
        applicationFlag = self.request.POST.get("applicationFlag")

        x0 = self.request.POST.get("x0")
        y0 = self.request.POST.get("y0")
        x1 = self.request.POST.get("x1")
        y1 = self.request.POST.get("y1")

        myWidth = 250
        myHeight = 400

        MethodView.methodName = self.request.POST.get("methodName")

        if(len(MethodView.fileCollectionNames)==0):
            i = 0
            MethodView.fileCollectionNames = []
            for item in MethodView.filesInputDetailsName:
                MethodView.fileCollectionNames.append(self.request.POST.get("fileCollection"+str(i)))
                i = i + 1

        if(len(MethodView.folderCollectionNames)==0):
            i = 0
            MethodView.folderCollectionNames = []
            for item in MethodView.foldersInputDetailsName:
                MethodView.folderCollectionNames.append(self.request.POST.get("folderCollection"+str(i)))
                i = i + 1


        finalStep = self.request.POST.get("finalStep")
        makeCollection = self.request.POST.get("makeCollection")
        newCollectionName = self.request.POST.get("newCollectionName")
        
        MethodView.images = MethodView.images
        
        selects = []
        numbers = []
        highlighters = []

        reqestMethodJson = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
        inputParams = reqestMethodJson.json()   

        #initialize backend input parameters
        for element in inputParams['input']:
            if 'select' in element:
                selects.append(element)
            if 'number' in element:
                numbers.append(element)
            if 'highlighter' in element:
                highlighters.append(element)

        
        MethodView.inputParams = inputParams
        MethodView.selects = selects
        MethodView.numbers = numbers
        MethodView.highlighters = highlighters

        showCollectionsForm = False
        showFilesForm = False

        if len(MethodView.highlighters) > 0 :
            MethodView.highlightersExist = True

        if len(MethodView.fileCollectionNames) > 1 or len(MethodView.folderCollectionNames) > 0:
            MethodView.multipleInput = True



        print("multiple: " + str(MethodView.multipleInput))
        print(MethodView.fileCollectionNames)
        print("highlighter exists: " + str(MethodView.highlightersExist))
        print(MethodView.highlighters)



        MethodView.isXML = False

        reqestMethodJson = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
        inputParams = reqestMethodJson.json()
        MethodView.inputParams = inputParams

        MethodView.colectionsFilesNames = []

        #overstep directly to step before application if there are no Collections for file input
        if((not MethodView.fileInput) and MethodView.folderInput):
            applicationFlag="True"

        if applicationFlag=="False" and finalStep!="True":

            #get names for files in each selected collection
            MethodView.imgNames = []
            for name in MethodView.fileCollectionNames:
                
                res = requests.get(diva+name)
                res = res.json()

                imgNames = []
                for element in res['files']:
                    temp = element['file']['identifier']
                    temp = temp.split("/")
                    imgNames.append(temp[1])

                MethodView.imgNames.append(imgNames)

            MethodView.colectionsFilesNames = zip(MethodView.fileCollectionNames, MethodView.imgNames)
            showFilesForm = True

        #By now we have selected the input collections and folders and selected files from the collectons
        if applicationFlag=="True" and finalStep!="True":  
            showFilesForm = False

            data = { "collections": [] }

            i = 0
            MethodView.imageFileNames = []
            MethodView.imagesUrls = []
            for name in MethodView.fileCollectionNames:

                data["collections"].append({"name": name, "files": []})

                res = requests.get(diva+name)
                res = res.json()

                filenames = self.request.POST.getlist("fileNames"+str(i))

                imageUrlsTemp = []
                for element in res['files']:
                    temp = element['file']['url']
                    temp = temp.split("/")
                    if temp[-1] in filenames:
                        imageUrlsTemp.append(element['file']['url'])
                        data["collections"][i]["files"].append({ "url": element['file']['url'], "filename": temp[-1]})
                        temp = temp[-1].split(".")
                        temp = temp[len(temp) - 1]
                        if temp != "png" and temp != "jpeg" and temp != "jpg" and temp != "JPG" and temp != "JPEG" and temp !="PNG":
                            MethodView.isXML = True

                MethodView.imageFileNames.append(filenames)
                MethodView.imagesUrls.append(imageUrlsTemp)

                i = i + 1

            MethodView.selectedInputJson = data
        
        if finalStep=="True": #apply method to selected images with set up input parameters and give option of saving images to a collection
            showFilesForm = False
            showCollectionsForm = False

            MethodView.selectedSelects = []
            MethodView.selectedNumbers = []
            MethodView.selectedHighlighters = []
            MethodView.resultingImages = []

            #YOU CAN ITERATE ONLY ONCE THROUGH A ZIP!
            MethodView.images = zip(MethodView.imagesUrls, MethodView.imageFileNames, MethodView.fileCollectionNames)

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

            

            index = 0
            for element in MethodView.highlighters:

                if index == 0 :
                    respo = requests.get(MethodView.imagesUrls[0][0])
                    img = Image.open(BytesIO(respo.content))
                    width, height = img.size
                    print("original size is: " + str(width) + " , " + str(height))

                    tempRatio = myHeight/myWidth

                    print("original h/w: " + str(height/width) + " compared to my h/w: " + str(tempRatio))

                    if height/width < tempRatio:
                        myHeight = height//(width/myWidth)
                        myHeight = int(myHeight)
                        print("Calculated height by ratio: " + str(myHeight))
                    else:
                        if height/width > tempRatio:
                            myWidth = width//(height/myHeight)
                            myWidth = int(myWidth)
                            print("Calculated width by ratio: " + str(myWidth))


                    tempX0 = int(x0) * (width//myWidth)
                    tempX1 = int(x1) * (width//myWidth)
                    tempY0 = int(y0) * (height//myHeight)
                    tempY1 = int(y1) * (height//myHeight)

                    x0 = str(tempX0) 
                    x1 = str(tempX1)
                    y0 = str(tempY0)
                    y1 = str(tempY1)

                data["parameters"]["highlighter"] = {
                    "type":"rectangle",
                    "closed": "true",
                    "segments":[
                    [x0,y0],
                    [x0,y1],
                    [x1,y1],
                    [x1,y0]
                  ]
                }
                index = index + 1

            MethodView.linksToResultingJson = []

            #print(MethodView.imagesUrls[0])

            #one file collection and no folder collections
            if MethodView.fileInput and MethodView.singleFileCollectionInput and not MethodView.folderInput:
                for element in MethodView.imagesUrls[0]:

                    tempName = element.split('/')
                    tempName = tempName[-1]

                    data["data"][0] = {
                        "inputImage": MethodView.fileCollectionNames[0] + "/" + tempName,
                    }

                    dataSend = json.dumps(data)
                    headers = {'Content-type': 'application/json'}
                    #print(url)
                    #print(dataSend)
                    responseToMethodApplication = requests.post("http://divaservices.unifr.ch/api/v2/"+url+"/1", data=dataSend, headers=headers)
                    responseToMethodApplication = responseToMethodApplication.json()
                    #responseToMethodApplication = {}
                    MethodView.responseToMethodApplication = responseToMethodApplication
                    #print("")
                    #print("Response of method application call:")
                    #print("")
                    #print(responseToMethodApplication)
                    #print("")
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
                        for element in resultingOutput['output']:
                            if 'file' in element:
                                if element['file']['options']['visualization'] == True:
                                    MethodView.resultingImages.append(element['file']['url'])
                                    MethodView.linksToResultingJson.append(resultingOutput['resultLink'])
                                #else :
                                    #if element['file']['options']['type'] != "logfile":
                                        #MethodView.resultingImages.append(element['file']['url'])
                                        #MethodView.linksToResultingJson.append(resultingOutput['resultLink'])

                        i = 0
                        MethodView.resultingFileNames=[]
                        #print(MethodView.imageFileNames)
                        for f in MethodView.resultingImages:
                            name = MethodView.imageFileNames[0][i].split(".")
                            name = name[0]
                            ext = f.split('/')
                            ext = ext[-1]
                            ext = ext.split('.')
                            ext = ext[1]

                            MethodView.resultingFileNames.append(name + "." + ext)

                            i=i+1

                        MethodView.resultingImagesZip = zip(MethodView.resultingImages,MethodView.linksToResultingJson,MethodView.resultingFileNames)

                    else: 
                        if 'errorType' in responseToMethodApplication:

                            print("")
                            print("ERROR BRANCH LINE 299 IN METHODVIEW.PY - SOMETHING IS BAD IN THE SENDING REQUEST (FILE NUMBER ETC..)")
                            print("")
                            print(responseToMethodApplication)
                            print("")

                            MethodView.linksToResultingJson.append(responseToMethodApplication['message'])
                            MethodView.resultingImages.append(responseToMethodApplication['message'])
            
            else:
                #if multiple file collections and/or there are folder collections, then single input per every collection
                #MethodView.selectedInputJson - contains collections: {[ { name(collName), files: [{filenames, url}] } ]}
                if (MethodView.fileInput and not MethodView.singleFileCollectionInput) or MethodView.folderInput:

                        index = 0
                        for collection in MethodView.selectedInputJson['collections']:

                            if collection['name'] in MethodView.fileCollectionNames:
                                print(collection)

                                element = collection['files'][0]['url']

                                print(element)

                                tempName = element.split('/')
                                tempName = tempName[-1]

                                data["data"][0][MethodView.filesInputDetailsName[index]] = collection['name'] + "/" + tempName

                            index = index + 1

                        if MethodView.folderInput:
                            index = 0
                            for collection in MethodView.folderCollectionNames:

                                data["data"][0][MethodView.foldersInputDetailsName[index]] = collection

                                index = index + 1

                        dataSend = json.dumps(data)
                        headers = {'Content-type': 'application/json'}
                        print(url)
                        print(dataSend)
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

                            print("")
                            print(resultingOutput)
                            print("")

                            while (resultingOutput['status'] == 'planned'):
                                print('waiting on server..')
                                resultingOutput = requests.get(responseToMethodApplication["results"][0]["resultLink"])
                                resultingOutput = resultingOutput.json()

                            print(resultingOutput)

                            for element in resultingOutput['output']:
                                if 'file' in element:
                                    if element['file']['options']['visualization'] == True:
                                        MethodView.resultingImages.append(element['file']['url'])
                                        MethodView.linksToResultingJson.append(resultingOutput['resultLink'])
                                    #else :
                                        #if element['file']['options']['type'] != "logfile":
                                           #MethodView.resultingImages.append(element['file']['url'])
                                            #MethodView.linksToResultingJson.append(resultingOutput['resultLink'])

                            i = 0
                            MethodView.resultingFileNames=[]
                            print(MethodView.imageFileNames)
                            for f in MethodView.resultingImages:
                                name = MethodView.imageFileNames[0][i].split(".")
                                name = name[0]
                                ext = f.split('/')
                                ext = ext[-1]
                                ext = ext.split('.')
                                ext = ext[1]
                                MethodView.resultingFileNames.append(name + "." + ext)
                                i=i+1
                            MethodView.resultingImagesZip = zip(MethodView.resultingImages,MethodView.linksToResultingJson,MethodView.resultingFileNames)
                        else: 
                            if 'errorType' in responseToMethodApplication:

                                print("")
                                print("ERROR BRANCH LINE 299 IN METHODVIEW.PY - SOMETHING IS BAD IN THE SENDING REQUEST")
                                print("")
                                print(responseToMethodApplication)
                                print("")

                                MethodView.linksToResultingJson.append(responseToMethodApplication['message'])
                                MethodView.resultingImages.append(responseToMethodApplication['message'])


                        

                

        #Method applied and here we make a new collection with a chosen name, containing the results
        if makeCollection == 'True':
            num = len(MethodView.resultingImages)
            i = 0
            #print(MethodView.resultingFileNames)
            for f in MethodView.resultingImages:
                print(f)
                if i==0:

                    array = MethodView.resultingFileNames[i].split('.')
                    filename = array[0]
                    ext = array[1]

                    data = {
                        "name": newCollectionName,
                        "files": [
                            {
                                "type": "url",
                                "value": f,
                                "name": filename,
                                "extension": ext
                            },
                        ]
                    }
                    data = json.dumps(data)
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(diva, data=data, headers=headers)
                else:

                    array = MethodView.resultingFileNames[i].split('.')
                    filename = array[0]
                    ext = array[1]

                    data = {
                        "name": newCollectionName,
                        "files": [
                            {
                                "type": "url",
                                "value": f,
                                "name": filename,
                                "extension": ext
                            },
                        ]
                    }
                    data = json.dumps(data)
                    headers = {'Content-type': 'application/json'}

                    response = requests.put(diva + newCollectionName, data=data, headers=headers)

                i = i + 1
                if i == num:
                    sleep(1)
                    return HttpResponseRedirect("/collection/"+newCollectionName)

        result = requests.get("http://divaservices.unifr.ch/api/v2/"+url+"/1")
        result = result.json()

        detailsKeys = []
        detailsValues = []

        for element in result['general'].keys():
            detailsKeys.append(element)

        for element in result['general'].values():
            detailsValues.append(element)

        MethodView.details = zip(detailsKeys, detailsValues)

        payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}

        context = {
            "details": MethodView.details,
            "methodName": MethodView.methodName,
            "showCollectionsForm": showCollectionsForm,
            "showFilesForm": showFilesForm,
            "imgNames": MethodView.imgNames,
            "selectedInputJson": MethodView.selectedInputJson,
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
            "fileCollectionNames": MethodView.fileCollectionNames,
            "folderCollectionNames": MethodView.folderCollectionNames,
            "colectionsFilesNames": MethodView.colectionsFilesNames,
            "highlightersExist": MethodView.highlightersExist,
            "multipleInput": MethodView.multipleInput,
        }
        return render(request, "method.html", context)