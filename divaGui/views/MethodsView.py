from divaGui.viewImports import *

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