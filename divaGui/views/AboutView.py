from divaGui.viewImports import *

class AboutView(View):
    def get(self, request, *args, **kwargs):

        context = {}

        return render(request, "about.html", context)