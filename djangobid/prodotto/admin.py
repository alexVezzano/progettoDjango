from django.contrib import admin
from .models import Prodotto

@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descrizione','categoria']

admin.register(Prodotto,ProdottoAdmin)