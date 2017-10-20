from divaGui.viewImports import *

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
                sleep(1)
                return HttpResponseRedirect("/collection/"+name)

    context = {

    }

    return render(request, 'add_collections.html', context)