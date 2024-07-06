from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from utente.models import Utente  
from .models import Asta, Prodotto
from django.utils import timezone
import datetime
import os

@override_settings(MEDIA_ROOT='/tmp/djangobid_test_media/')
class CreaAstaViewTest(TestCase):
    def setUp(self):
        self.user = Utente.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Immagine default per un prodotto
        immagine_path = os.path.join(os.path.dirname(__file__), 'default_image.jpg')
        with open(immagine_path, 'rb') as f:
            self.immagine = SimpleUploadedFile(name='test_image.jpg', content=f.read(), content_type='image/jpeg')

    def test_crea_asta_accesso(self):
        response = self.client.get(reverse('asta:crea_asta'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crea_asta.html')

    #test creazione con dati corretti
    def test_crea_asta_form(self):
        prodotto_data = {
            'nome': 'Prodotto di Test',
            'descrizione': 'Descrizione del prodotto di test',
            'categoria': 'ELETTRONICA',
            'immagine': self.immagine
        }
        asta_data = {
            'prezzo_di_partenza': 100.00,
            'end_time': (timezone.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        }
        response = self.client.post(reverse('asta:crea_asta'), prodotto_data | asta_data)

        # Test del reindirizzamento
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.url)  

        # Dopo il reindirizzamento, verifica l'oggetto creato nel database
        self.assertTrue(Prodotto.objects.filter(nome='Prodotto di Test').exists())
        asta = Asta.objects.get(prodotto__nome='Prodotto di Test')
        self.assertEqual(asta.venditore, self.user)
        self.assertEqual(asta.prodotto.nome, 'Prodotto di Test')

    #test creazione con nome inesistente
    def test_crea_asta_nome_inesistente(self):
        prodotto_data = {
            'nome': '',  # Nome vuoto
            'descrizione': 'Descrizione del prodotto di test',
            'categoria': 'ELETTRONICA',
            'immagine': self.immagine
        }
        asta_data = {
            'prezzo_di_partenza': 100.00,  
            'end_time': (timezone.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')  
        }
        response = self.client.post(reverse('asta:crea_asta'), prodotto_data | asta_data)

        # Verifica che non ci sia stato il reindirizzamento, poiché il form non è valido
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crea_asta.html')

        # Verifica che l'oggetto Prodotto non sia stato creato
        self.assertFalse(Prodotto.objects.filter(nome='').exists())
        self.assertFalse(Asta.objects.filter(prezzo_di_partenza=100.00).exists())

    #test creazione con data passata
    def test_crea_asta_data_passata(self):
        prodotto_data = {
            'nome': 'prova', 
            'descrizione': 'Descrizione del prodotto di test',
            'categoria': 'ELETTRONICA',
            'immagine': self.immagine
        }
        asta_data = {
            'prezzo_di_partenza': 100.00,  
            'end_time': (timezone.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')    #data antecedente ad oggi
        }
        response = self.client.post(reverse('asta:crea_asta'), prodotto_data | asta_data)

        # Verifica che non ci sia stato il reindirizzamento, poiché il form non è valido
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crea_asta.html')

        # Verifica che l'oggetto Prodotto non sia stato creato
        self.assertFalse(Prodotto.objects.filter(nome='prova').exists())
        self.assertFalse(Asta.objects.filter(prezzo_di_partenza=100.00).exists())


    #test creazione prezzo negativo
    def test_crea_asta_prezzo_negativo(self):
        prodotto_data = {
            'nome': 'prova', 
            'descrizione': 'Descrizione del prodotto di test',
            'categoria': 'ELETTRONICA',
            'immagine': self.immagine                
        }
        asta_data = {
            'prezzo_di_partenza': -100.00,      #prezzo negativo
            'end_time': (timezone.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')  
        }
        response = self.client.post(reverse('asta:crea_asta'), prodotto_data | asta_data)

        # Verifica che non ci sia stato il reindirizzamento, poiché il form non è valido
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crea_asta.html')

        # Verifica che l'oggetto Prodotto non sia stato creato
        self.assertFalse(Prodotto.objects.filter(nome='prova').exists())
        self.assertFalse(Asta.objects.filter(prezzo_di_partenza=100.00).exists())

    #test creazione senza immagine
    def test_crea_asta_senza_immagine(self):
        prodotto_data = {
            'nome': 'prova', 
            'descrizione': 'Descrizione del prodotto di test',
            'categoria': 'ELETTRONICA',
            'immagine': ''                #immagine non presente
        }
        asta_data = {
            'prezzo_di_partenza': 100.00,  
            'end_time': (timezone.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')  
        }
        response = self.client.post(reverse('asta:crea_asta'), prodotto_data | asta_data)

        # Verifica che non ci sia stato il reindirizzamento, poiché il form non è valido
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crea_asta.html')

        # Verifica che l'oggetto Prodotto non sia stato creato
        self.assertFalse(Prodotto.objects.filter(nome='prova').exists())
        self.assertFalse(Asta.objects.filter(prezzo_di_partenza=100.00).exists())