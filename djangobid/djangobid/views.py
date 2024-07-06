from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from asta.models import Asta, Offerta  # Importa il modello Offerta
from prodotto.models import Prodotto
from django.core.paginator import Paginator
from collections import Counter

def home(request):
    # Recupera tutte le aste disponibili
    #aste = Asta.objects.all()
    #recupera solo le aste ancora attive
    aste = Asta.objects.filter(is_active=True)

    # Filtra per categoria se specificato
    categoria_selezionata = request.GET.get('categoria')
    if categoria_selezionata:
        aste = aste.filter(prodotto__categoria=categoria_selezionata)
    
    # Filtra per query di ricerca se specificato
    query = request.GET.get('query')
    if query:
        aste = aste.filter(prodotto__nome__icontains=query)

    # Reccomendation system --> basato sulle categorie dei prodotti per cui l'utente ha effettuato offerte
    if request.user.is_authenticated:
        offerte_utente = Offerta.objects.filter(profilo=request.user)
        categorie_preferite = Counter(offerta.asta.prodotto.categoria for offerta in offerte_utente)
        categorie_ordinate = [categoria for categoria, _ in categorie_preferite.most_common()]
    else:
        categorie_ordinate = []

    # Separazione delle aste in raccomandate e non raccomandate
    if categorie_ordinate:
        aste_raccomandate = sorted(
            aste.filter(prodotto__categoria__in=categorie_ordinate), 
            key=lambda asta: categorie_ordinate.index(asta.prodotto.categoria)
        )
        aste_non_raccomandate = aste.exclude(prodotto__categoria__in=categorie_ordinate).order_by('end_time')
        aste_ordinate = aste_raccomandate + list(aste_non_raccomandate)
    else:
        aste_ordinate = aste.order_by('end_time')

    # visualizzo 12 aste per pagina della homepage
    paginator = Paginator(aste_ordinate, 12)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Crea un contesto per ogni asta con il prezzo corrente
    aste_con_prezzo = []
    for asta in page_obj:
        highest_bid = asta.offerte.order_by('-valore_offerta').first()
        if highest_bid:
            prezzo_corrente = highest_bid.valore_offerta
        else:
            prezzo_corrente = asta.prezzo_di_partenza
        aste_con_prezzo.append({'asta': asta, 'prezzo_corrente': prezzo_corrente})
    
    # Passa le aste al template
    context = {
        'aste_con_prezzo': aste_con_prezzo,
        'page_obj': page_obj,
        'categorie': Prodotto.CATEGORIE,
        'categoria_selezionata': categoria_selezionata,
        'query': query,
    }
    return render(request, 'home.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home')