from django.test import TestCase
from django.urls import reverse
from .models import Utente  # Importa il modello Utente
from .forms import RegistrazioneUtenteForm

class RegistrazioneUtenteTest(TestCase):
    #test registrazione corretta
    def test_registrazione_successo(self):
        form_data = {
            'username': 'testuser',
            'password1': 'Ciaociao1',
            'password2': 'Ciaociao1',
            'email': 'testuser@example.com',
            'nome':'test',
            'cognome':'user'
        }
        form = RegistrazioneUtenteForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('utente:registrazione'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect dopo registrazione
        self.assertTrue(Utente.objects.filter(username='testuser').exists()) 

    #test registrazione con le due password che non coincidono
    def test_registrazione_password_non_coincidente(self):
        form_data = {
            'username': 'testuser',
            'password1': 'Ciaociao1',
            'password2': 'Ciaociao2',  # Password non coincidente
            'email': 'testuser@example.com',
            'nome':'test',
            'cognome':'user'
        }
        form = RegistrazioneUtenteForm(data=form_data)
        self.assertFalse(form.is_valid())

    #test restigrazione con un'email non valida
    def test_registrazione_email_non_valida(self):
        form_data = {
            'username': 'testuser',
            'password1': 'Ciaociao1',
            'password2': 'Ciaociao1',
            'email': '',  # Email non valida
            'nome':'test',
            'cognome':'user'
        }
        form = RegistrazioneUtenteForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    #test resgistrazione con un username già presente
    def test_registrazione_utente_presente(self):
        Utente.objects.create_user(username='testuser1', password='password')
        form_data = {
            'username': 'testuser1',
            'password1': 'Ciaociao1',
            'password2': 'Ciaociao1',
            'email': 'test@example.com', 
            'nome':'luca',
            'cognome':'user'
        }
        form = RegistrazioneUtenteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFalse(Utente.objects.filter(nome='luca').exists()) 
