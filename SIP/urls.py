from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views.cocktail_detail_view import AddReviewView, AddStarView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('cocktail/<int:pk>/', views.MyCocktailView.as_view(), name='cocktail_detail'),
    path('cocktail/<int:pk>/add_review/', AddReviewView.as_view(), name='add_review'),
    path('cocktail/<int:pk>/add_star/', AddStarView.as_view(), name='add_star'),
    path('cocktail/', RedirectView.as_view(url="/SIP/")),
]
