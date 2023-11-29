# views.py
from django.shortcuts import render, redirect
from django.views import View
from ..forms import CocktailForm, CocktailIngredientFormSet


class CreateCocktail(View):
    template_name = 'sip/upload_image.html'

    def get(self, request, *args, **kwargs):
        cocktail_form = CocktailForm()
        ingredient_formset = CocktailIngredientFormSet(prefix='ingredient')

        return render(request, self.template_name, {
            'cocktail_form': cocktail_form,
            'ingredient_formset': ingredient_formset,
        })

    def post(self, request, *args, **kwargs):
        cocktail_form = CocktailForm(request.POST, request.FILES)
        ingredient_formset = CocktailIngredientFormSet(request.POST,
                                                       prefix='ingredient')

        if cocktail_form.is_valid() and ingredient_formset.is_valid():
            # Process the forms and save data
            cocktail = cocktail_form.save()
            ingredient_formset.instance = cocktail
            ingredient_formset.save()
            return redirect('SIP:index')

        return render(request, self.template_name, {
            'cocktail_form': cocktail_form,
            'ingredient_formset': ingredient_formset,
        })
