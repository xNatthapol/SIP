from django.shortcuts import render, redirect
from django.views import View
from ..models import FavouriteCocktail, FavouriteIngredient, Cocktail, Ingredient


class AddToFavouritesView(View):
    template_name = 'sip/favourite_list.html'

    def post(self, request, model_type, pk):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if user is not authenticated

        user = request.user
        model_class = None

        if model_type == 'cocktail':
            model_class = Cocktail
            favourite_model = FavouriteCocktail
        elif model_type == 'ingredient':
            model_class = Ingredient
            favourite_model = FavouriteIngredient
        else:
            # Handle invalid model_type, you can customize this part based on your needs
            return render(request, 'error.html', {'error_message': 'Invalid model type'})

        item = model_class.objects.get(pk=pk)

        # Check if the item is already in favourites
        if not favourite_model.objects.filter(user=user, **{f'{model_type}_id': pk}).exists():
            favourite_model.objects.create(user=user, **{f'{model_type}_id': pk})

        return redirect('SIP:favourite_list')

class FavouriteListView(View):
    template_name = 'sip/favourite_list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if user is not authenticated

        user = request.user
        favourite_cocktails = FavouriteCocktail.objects.filter(user=user)
        favourite_ingredients = FavouriteIngredient.objects.filter(user=user)

        context = {
            'favourite_cocktails': favourite_cocktails,
            'favourite_ingredients': favourite_ingredients,
        }

        return render(request, self.template_name, context)
