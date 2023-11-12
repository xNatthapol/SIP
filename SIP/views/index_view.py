import requests
from datetime import datetime, timezone
from django.utils import timezone
from SIP.models import Tag, Ingredient, CocktailIngredient, Cocktail
from django.views.generic import TemplateView
from django.shortcuts import render


class IndexView(TemplateView):
    template_name = "sip/index.html"
    cocktail_api = "SIP.CocktailApi"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cocktails'] = Cocktail.objects.all()
        context['tags'] = Tag.objects.all()
        context['ingredients'] = Ingredient.objects.all()
        return context
    
    def get(self, request, *args, **kwargs):
        if request.GET.get('search'):
            search = request.GET.get('search')
            context = self.get_context_data(**kwargs)
            context['cocktails'] = Cocktail.objects.filter(name__icontains=search)
            return render(request, self.template_name, context)
        else:
            return super().get(request, *args, **kwargs)
