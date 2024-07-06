from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password 
from .models import Utente
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class RegistrazioneUtenteForm(UserCreationForm):
    password2 = forms.CharField(label='Conferma password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'nome', 'cognome', 'password1', 'password2', 'email']
        widgets = {
            'password1': forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Username già utilizzato.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email già utilizzata.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Le password non corrispondono.")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password1'])  # Crittografa la password
        if commit:
            user.save()
        return user
    


class ModificaProfiloUtenteForm(UserChangeForm):
    password = None  # Rimuove il campo password

    class Meta:
        model = Utente
        fields = ['nome', 'cognome', 'email', 'username', 'indirizzo', 'città', 'numero_telefono', 'immagine_profilo']

    def __init__(self, *args, **kwargs):
        super(ModificaProfiloUtenteForm, self).__init__(*args, **kwargs)
        # Rende i campi non modificabili
        self.fields['email'].disabled = True
        self.fields['nome'].disabled = True
        self.fields['cognome'].disabled = True

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salva modifiche'))

    def clean_email(self):
        return self.instance.email  # Restituisce l'email originale, rendendola non modificabile

    def clean_nome(self):
        return self.instance.nome  # Restituisce il nome originale, rendendolo non modificabile

    def clean_cognome(self):
        return self.instance.cognome  # Restituisce il cognome originale, rendendolo non modificabile