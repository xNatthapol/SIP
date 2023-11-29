from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.shortcuts import get_object_or_404

from ..models import FavouriteCocktail, FavouriteIngredient, Cocktail, Ingredient


class AddToFavouritesView(View):
    template_name = 'sip/favourite_list.html'

    def get(self, request, model_type, pk):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if the user is not authenticated

        user = request.user
        model_class = None
        action = request.GET.get('action')

        if action == 'add':
            if model_type == 'cocktail':
                model_class = Cocktail
                favourite_model = FavouriteCocktail
            elif model_type == 'ingredient':
                model_class = Ingredient
                favourite_model = FavouriteIngredient
            else:
                # Handle an invalid model_type, customize this part based on your needs
                return render(request, 'error.html', {'error_message': 'Invalid model type'})

        # Use get_object_or_404 to raise a 404 error if the object is not found
        item = get_object_or_404(model_class, pk=pk)

        # Check if the item is already in favourites
        favourite_entry = favourite_model.objects.filter(user=user, **{f'{model_type}_id': pk}).first()

        try:
            if favourite_entry:
                # If the item is already in favourites, remove it
                favourite_entry.delete()
            else:
                # If the item is not in favourites, add it
                favourite_model.objects.create(user=user, **{f'{model_type}_id': pk})
        except Exception as e:
            print(f'Error deleting item from favourites: {e}')

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

