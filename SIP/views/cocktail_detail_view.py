# views.py
from django.core.exceptions import ValidationError
from django.db.models import Avg, DecimalField
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from ..models import Cocktail, Review, Star
from ..forms import ReviewForm, StarForm


class CocktailDetailView(View):
    template_name = 'sip/cocktail_detail.html'

    def get(self, request, pk):
        cocktail = Cocktail.objects.get(pk=pk)
        # Fetch reviews for the cocktail
        reviews = Review.objects.filter(cocktail=cocktail)
        # Calculate average score for the cocktail
        queryset = Star.objects.filter(cocktail=cocktail).aggregate(Avg('score'))['score__avg']
        average_score = round(queryset, 2) if queryset else None
        rating = self.calculate_star_rating(average_score)

        # Initialize the forms
        star_form = StarForm()
        comment_form = ReviewForm()

        context = {
            'cocktail': cocktail,
            'star_rating': rating,
            'reviews': reviews,
            'average_score': average_score,
            'star_form': star_form,
            'comment_form': comment_form,
        }

        return render(request, self.template_name, context)

    def calculate_star_rating(self, average_score):
        # Customize this function based on your design for star ratings
        if average_score is not None:
            digit = int(average_score)
            integer_part = [1] * digit
            fractional_part = average_score - digit
            if fractional_part == 0:
                fractional_part = None
            return integer_part, fractional_part
        return None


class AddReviewView(View):
    template_name = 'sip/cocktail_detail.html'

    def post(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.cocktail = cocktail
            review.user = request.user  # Assuming you have user authentication
            review.save()
            return redirect(reverse('cocktail_detail', args=[pk]))
        else:
            # Handle invalid form by rendering the template with the form
            context = {
                'cocktail': cocktail,
                'form': form,
            }
            return render(request, self.template_name, context)


class AddStarView(View):
    template_name = 'sip/cocktail_detail.html'

    def post(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)

        form = StarForm(request.POST)

        if form.is_valid():
            star = form.save(commit=False)
            star.cocktail = cocktail
            star.user = request.user  # Assuming you have user authentication
            star.save()
            return redirect(reverse('cocktail_detail', args=[pk]))
        else:
            # Handle invalid form by rendering the template with the form
            context = {
                'cocktail': cocktail,
                'form': form,
            }
            return render(request, self.template_name, context)
