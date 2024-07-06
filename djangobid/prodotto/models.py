from django.db import models

class Prodotto(models.Model):
    CATEGORIE = [
        ('ELETTRONICA', 'Elettronica'),
        ('ABBIGLIAMENTO', 'Abbigliamento'),
        ('CASA', 'Casa'),
        ('SPORT', 'Sport'),
        ('GIOCHI', 'Giochi'),
        ('LIBRI', 'Libri'),
    ]

    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIE)
    immagine = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.nome