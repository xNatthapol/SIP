from django.urls import path
from django.views.generic import RedirectView
from . import views


app_name = "SIP"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('cocktail/<int:pk>/', views.CocktailDetailView.as_view(), name='cocktail_detail'),
    path('cocktail/<int:pk>/add_review/', views.AddReviewView.as_view(), name='add_review'),
    path('cocktail/<int:pk>/add_star/', views.AddStarView.as_view(), name='add_star'),
    path('cocktail/', RedirectView.as_view(url="/SIP/")),
    path('ingredient/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredient_detail'),
    path('ingredient/', RedirectView.as_view(url="/SIP/")),
    path('upload_image/', views.CreateCocktail.as_view(), name='upload_image'),
    path('game/', views.GameView.as_view(), name='game'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('all_ingredient/', views.all_ingred, name='all_ingred'),
]
