from divaGui.viewImports import *

class TryoutsTemplateView(TemplateView):
    template_name = 'tryouts.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TryoutsTemplateView,
                        self).get_context_data(*args, **kwargs)

        # OVDE JE TELO VIEW-A

        return context