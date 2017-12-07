from divaGui.viewImports import *

class HighlighterView(View):
	def get(self, request, *args, **kwargs):

		context = {}

		return render(request, "highlighter.html", context)

	def post(self, request, *args, **kwargs):
		

		context = {}

		return HttpResponseRedirect("/method/")