from django.urls import path
from . import views

app_name = 'asta'

urlpatterns = [
    path('crea/', views.crea_asta, name='crea_asta'),
    path('<int:asta_id>/', views.partecipa_asta, name='partecipa_asta'),
    path('mieaste/', views.mie_aste, name='mie_aste'),  # Nuova URL per le mie aste
    path('venditore/<int:venditore_id>/', views.visualizza_venditore, name='visualizza_venditore'),
    path('asta_conclusa/<int:asta_id>/', views.asta_conclusa, name='asta_conclusa'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('countdown/<int:asta_id>/', views.countdown, name='countdown'),

]