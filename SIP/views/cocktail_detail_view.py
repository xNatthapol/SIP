from django.views.generic import DetailView
from SIP.models import Cocktail

class CocktailDetailView(DetailView):
    model = Cocktail
    template_name = 'sip/cocktail_detail.html'
    context_object_name = 'cocktail'
