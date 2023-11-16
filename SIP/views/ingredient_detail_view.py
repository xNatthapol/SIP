from django.views.generic import DetailView
from SIP.models import Ingredient


class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = 'sip/ingredient_detail.html'
    context_object_name = 'ingredient'
