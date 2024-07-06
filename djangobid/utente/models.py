from django.db import models
from django.contrib.auth.models import AbstractUser

class Utente(AbstractUser):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    indirizzo = models.CharField(max_length=255, blank=True, null=True)
    città = models.CharField(max_length=100, blank=True, null=True)
    numero_telefono = models.CharField(max_length=20, blank=True, null=True)
    immagine_profilo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
