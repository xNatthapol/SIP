import random
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from SIP.models import Player, Ingredient, Cocktail


@method_decorator(login_required, name='dispatch')
class GameView(View):
    template_name = 'SIP/game.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = None

    def get(self, request):
        player, created = Player.objects.get_or_create(user=request.user)
        random_cocktail = random.choice(Cocktail.objects.all())
        ingredients = Ingredient.objects.all()
        ingredients_list = []
        for ingredient_cocktail in random_cocktail.ingredients.all():
            ingredients_list.append(ingredient_cocktail)
        count = 0
        for _ in range(len(ingredients)):
            if count == 3:
                break
            random_ingredient = random.choice(ingredients)
            if random_ingredient not in ingredients_list:
                ingredients_list.append(random_ingredient)
                count += 1
        random.shuffle(ingredients_list)
        context = {
            'cocktail': random_cocktail,
            'ingredients': ingredients_list,
            'player': player,
        }
        request.session.pop('score_added', None)
        request.session.pop('reload_next_question', None)
        return render(request, self.template_name, context)

    def post(self, request):
        selected_values = request.POST.getlist('ingredients')
        cocktail_id = request.POST.get('cocktail_id')

        if 'reload_next_question' in request.session and request.session['reload_next_question'] == True:
            return redirect(reverse('game'))
        cocktail = Cocktail.objects.get(id=cocktail_id)
        ingredients = cocktail.ingredients.all()
        selected_values = list(map(int, selected_values))
        correct_ingredients = []
        for ingredient in ingredients:
            correct_ingredients.append(ingredient.id)
        correct_ingredients.sort()
        selected_values.sort()
        if 'score_added' in request.session:
            score = 0
            context = {'score': score}
            return render(request, 'SIP/success_game.html', context)
        if selected_values == correct_ingredients:
            player = Player.objects.get(user=request.user)
            score = len(correct_ingredients) * 20
            player.score += score
            player.save()
            context = {'score': score}
            request.session['score_added'] = True
            request.session['reload_next_question'] = True
            return render(request, 'SIP/success_game.html', context)
        total_score = 0
        for ingredient in selected_values:
            if ingredient in correct_ingredients:
                total_score += 10
        player = Player.objects.get(user=request.user)
        player.score += total_score
        player.save()
        context = {"score": total_score}
        request.session['score_added'] = True
        request.session['reload_next_question'] = True
        return render(request, 'SIP/success_game.html', context)


class LeaderboardView(View):
    template_name = 'SIP/leaderboard.html'

    def get(self, request):
        players = Player.objects.order_by('-score')
        return render(request, self.template_name, {'players': players})
