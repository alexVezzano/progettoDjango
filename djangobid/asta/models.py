from django.db import models
from django.conf import settings
from prodotto.models import Prodotto
from django.core.validators import MinValueValidator, MaxValueValidator



class Asta(models.Model):
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE, related_name='aste')
    venditore = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='aste')
    prezzo_di_partenza = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Asta per {self.prodotto.nome}"

class Offerta(models.Model):
    asta = models.ForeignKey(Asta, on_delete=models.CASCADE, related_name='offerte')
    profilo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offerte')
    valore_offerta = models.DecimalField(max_digits=10, decimal_places=2)
    orario_offerta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offerta di {self.valore_offerta} per {self.asta.prodotto.nome} da {self.profilo.username}"
    


class Recensione(models.Model):
    mittente = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recensioni_inviate', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recensioni_ricevute', on_delete=models.CASCADE)
    asta = models.ForeignKey('Asta', on_delete=models.CASCADE, related_name='recensioni')
    valutazione = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    descrizione = models.TextField()

    class Meta:
        unique_together = ('mittente', 'destinatario', 'asta')

    def __str__(self):
        return f'Recensione di {self.mittente.username} per {self.destinatario.username} - Valutazione: {self.valutazione}'