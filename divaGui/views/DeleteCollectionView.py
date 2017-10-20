from divaGui.viewImports import *

class DeleteCollectionView(View):
	def get(self, request, *args, **kwargs):

		context = {}

		return render(request, "delete_collection.html", context)

	def post(self, request, *args, **kwargs):
		name = self.request.POST.get("name")

		payload = {'some': 'data'}
		headers = {'content-type': 'application/json'}
		response = requests.delete(
			diva + name, data=json.dumps(payload), headers=headers)

		context = {}

		return HttpResponseRedirect("/collections/")

