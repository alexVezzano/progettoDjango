from django.contrib import admin
from .models import Asta, Offerta,Recensione

@admin.register(Asta)
class AstaAdmin(admin.ModelAdmin):
    list_display = ['prodotto', 'venditore', 'prezzo_di_partenza', 'start_time', 'end_time', 'is_active']

@admin.register(Offerta)
class OffertaAdmin(admin.ModelAdmin):
    list_display = ['asta', 'profilo', 'valore_offerta', 'orario_offerta']

@admin.register(Recensione)
class RecensioneAdmin(admin.ModelAdmin):
    list_display=['mittente','destinatario','asta','valutazione','descrizione']

admin.register(Asta,AstaAdmin)
admin.register(Offerta,OffertaAdmin)
admin.register(Recensione,RecensioneAdmin)