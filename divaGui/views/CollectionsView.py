from divaGui.viewImports import *

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

    def post(self, request, *args, **kwargs):
        name = self.request.POST.get("name")
        # print(name)
        payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}
        response = requests.delete(
            diva + name, data=json.dumps(payload), headers=headers)
        context = {}
        return HttpResponseRedirect("/collections/")