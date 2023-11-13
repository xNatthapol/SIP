from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('cocktail/<int:pk>/', views.MyCocktailView.as_view(), name='cocktail_detail'),
    path('cocktail/', RedirectView.as_view(url="/SIP/")),
]
