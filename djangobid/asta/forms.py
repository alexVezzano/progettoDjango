from django import forms
from prodotto.models import Prodotto
from .models import Asta,Offerta,Recensione
from django.utils import timezone


class ProdottoForm(forms.ModelForm):
    class Meta:
        model = Prodotto
        fields = ['nome', 'descrizione', 'categoria', 'immagine']

class AstaForm(forms.ModelForm):
    class Meta:
        model = Asta
        fields = ['prezzo_di_partenza', 'end_time']
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        now = timezone.now()

        if end_time <= now:
            raise forms.ValidationError("La data deve essere successiva a quella attuale.")
        
        if end_time.date() == now.date() and end_time.time() <= now.time():
            raise forms.ValidationError("L'orario di fine deve essere successivo all'orario attuale.")

        return end_time

    def clean_prezzo_di_partenza(self):
        prezzo_di_partenza = self.cleaned_data.get('prezzo_di_partenza')
        if prezzo_di_partenza <= 0:
            raise forms.ValidationError("Il prezzo di partenza deve essere un valore positivo.")
        return prezzo_di_partenza

   
class OffertaForm(forms.ModelForm):
    valore_offerta = forms.DecimalField(label='Valore dell\'offerta', min_value=0)

    class Meta:
        model = Offerta
        fields = ['valore_offerta']

    def __init__(self, *args, asta=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.asta = asta

    def clean_valore_offerta(self):
        valore_offerta = self.cleaned_data.get('valore_offerta')
        if self.asta is None:
            raise forms.ValidationError("Impossibile trovare l'asta correlata a questa offerta.")
        highest_bid = self.asta.offerte.order_by('-valore_offerta').first()
        if highest_bid and valore_offerta <= highest_bid.valore_offerta:
            raise forms.ValidationError("L'offerta deve essere superiore all'offerta attuale più alta.")

        if valore_offerta <= self.asta.prezzo_di_partenza:
            raise forms.ValidationError("L'offerta deve essere superiore al prezzo di partenza.")

        return valore_offerta
    


class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = ['valutazione', 'descrizione']
        widgets = {
            'valutazione': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'descrizione': forms.Textarea(attrs={'rows': 4}),
        }


