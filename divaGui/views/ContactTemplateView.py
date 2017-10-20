from divaGui.viewImports import *

class ContactTemplateView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ContactTemplateView,
                        self).get_context_data(*args, **kwargs)

        # OVDE JE TELO VIEW-A

        return context


#class ContactView(View):
#    def get(self, request, *args, **kwargs):
#
#        context = {}
#
#        return render(request, "contact.html", context)
