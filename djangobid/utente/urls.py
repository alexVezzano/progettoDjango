from django.urls import path
from . import views


app_name="utente"


urlpatterns = [
    path('registrazione/', views.registrazione, name='registrazione'),
    path('login/', views.login, name='login'),
    path('profilo/', views.profilo, name='profilo'),  
    path('profilo/modifica/', views.modifica_profilo, name='modifica_profilo'),  
]