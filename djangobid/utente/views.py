from django.shortcuts import render, redirect
from .forms import RegistrazioneUtenteForm,ModificaProfiloUtenteForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Utente
from asta.models import Recensione
from django.contrib import messages




def registrazione(request):
    if request.method == 'POST':
        form = RegistrazioneUtenteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('utente:login')  # Reindirizzamento dopo la registrazione
    else:
        form = RegistrazioneUtenteForm()
    return render(request, 'registrazione.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Reindirizza alla homepage dopo il login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profilo(request):
    recensioni = Recensione.objects.filter(destinatario=request.user).select_related('mittente', 'asta__prodotto').values('mittente__username', 'valutazione', 'descrizione', 'asta__prodotto__nome','asta__id')
    media_valutazioni = recensioni.aggregate(media=Avg('valutazione'))['media']
    return render(request, 'profilo.html', {
        'user': request.user,
        'recensioni': list(recensioni),  # Convertiamo in lista per il template
        'media_valutazioni': media_valutazioni,
    })


@login_required
def modifica_profilo(request):
    if request.method == 'POST':
        form = ModificaProfiloUtenteForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo modificato con successo!')
            return redirect('utente:profilo')
    else:
        form = ModificaProfiloUtenteForm(instance=request.user)
    return render(request, 'modifica_profilo.html', {'form': form})