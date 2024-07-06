from django.shortcuts import render, redirect,get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef, Max,Avg
from .forms import ProdottoForm, AstaForm,OffertaForm,RecensioneForm
from .models import Asta,Offerta,Recensione
from utente.models import Utente
from django.http import JsonResponse



@login_required
def crea_asta(request):
    if request.method == 'POST':
        prodotto_form = ProdottoForm(request.POST, request.FILES)
        asta_form = AstaForm(request.POST)

        if prodotto_form.is_valid() and asta_form.is_valid():
            prodotto = prodotto_form.save()
            asta = asta_form.save(commit=False)
            asta.prodotto = prodotto
            asta.venditore = request.user
            asta.start_time = timezone.now()
            asta.save()
            messages.success(request, "Asta creata con successo!")
            return redirect('home')
        
    else:
        prodotto_form = ProdottoForm()
        asta_form = AstaForm()

    context = {
        'prodotto_form': prodotto_form,
        'asta_form': asta_form
    }
    return render(request, 'crea_asta.html', context)

def partecipa_asta(request, asta_id):
    asta = get_object_or_404(Asta, pk=asta_id)
    highest_bid = asta.offerte.order_by('-valore_offerta').first()
    prezzo_iniziale = asta.prezzo_di_partenza if not highest_bid else highest_bid.valore_offerta
    is_asta_scaduta = asta.end_time <= timezone.now() or not asta.is_active

    highest_bidder = highest_bid.profilo if highest_bid else None
    is_highest_bidder = request.user == highest_bidder if request.user.is_authenticated else False

    # Calcola la scadenza da passare nel contesto
    now = timezone.now()
    is_time_remaining=False
    #se scade oggi voglio il tempo rimanente
    if asta.end_time.date() == now.date():
        time_remaining = asta.end_time - now
        formatted_end_time = "{:02d}:{:02d}:{:02d}".format(time_remaining.seconds // 3600, (time_remaining.seconds // 60) % 60, time_remaining.seconds % 60)
        is_time_remaining=True
    #se scade un altro giorno voglio l'end_time
    else:
        formatted_end_time = asta.end_time.strftime("%d/%m/%Y %H:%M")

    print(is_asta_scaduta)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = OffertaForm(request.POST, asta=asta)
            if form.is_valid():
                if is_asta_scaduta:
                    messages.error(request, "L'asta è scaduta o non è attiva.")
                    return redirect('asta:partecipa_asta', asta_id=asta.id)
                
                offerta = form.save(commit=False)
                offerta.asta = asta
                offerta.profilo = request.user

                if request.user == asta.venditore:
                    messages.error(request, "Non puoi fare un'offerta per un'asta che hai creato.")
                elif is_highest_bidder:
                    messages.error(request, "Non puoi fare un'offerta superiore alla tua offerta attuale.")
                else:
                    offerta.save()
                    return redirect('asta:partecipa_asta', asta_id=asta.id)
        else:
            return redirect('login')
    else:
        form = OffertaForm(asta=asta) if request.user.is_authenticated else None

    context = {
        'asta': asta,
        'highest_bid': highest_bid.valore_offerta if highest_bid else prezzo_iniziale,
        'highest_bidder': highest_bidder,
        'is_highest_bidder':is_highest_bidder,
        'formatted_end_time':formatted_end_time,
        'is_time_remaining':is_time_remaining,
        'form': form,
        'is_asta_scaduta': is_asta_scaduta,

    }
    return render(request, 'partecipa_asta.html', context)

@login_required
def mie_aste(request):
    utente = request.user

    # Aste create dall'utente
    aste_create_attive = Asta.objects.filter(venditore=utente, is_active=True)
    aste_create_concluse = Asta.objects.filter(venditore=utente, is_active=False).distinct()


    # Subquery per ottenere il profilo del massimo offerente per ogni asta
    max_offerta_subquery = Offerta.objects.filter(
        asta=OuterRef('pk')
    ).order_by('-valore_offerta').values('profilo__id')[:1]

    # Filtrare le aste dove il massimo offerente è l'utente specifico
    aste_vinte = Asta.objects.filter(
        is_active=False,
        id__in=Offerta.objects.filter(
            profilo=utente,
            asta__is_active=False
        ).values('asta_id').distinct()
    ).annotate(
        max_offerta_profilo=Subquery(max_offerta_subquery)
    ).filter(
        max_offerta_profilo=utente.id
    )

    # Aste in cui l'utente ha fatto un'offerta e sono ancora attive
    aste_offerte_attive = Asta.objects.filter(offerte__profilo=utente, is_active=True).distinct()

    context = {
        'aste_create_attive': aste_create_attive,
        'aste_create_concluse': aste_create_concluse,
        'aste_vinte': aste_vinte,
        'aste_offerte_attive': aste_offerte_attive,
    }

    return render(request, 'mie_aste.html', context)


def visualizza_venditore(request, venditore_id):
    venditore = get_object_or_404(Utente, pk=venditore_id)
    #Se l'utente loggato è lo stesso dell'utente venditore, allora reindirizzo a mie_aste
    if request.user.is_authenticated:
        if request.user == venditore:
            return redirect('asta:mie_aste')
       
    
    now = timezone.now()
    
    # Ottieni le aste attive del venditore
    aste_attive = Asta.objects.filter(venditore=venditore, is_active=True, end_time__gt=now)
    recensioni = Recensione.objects.filter(destinatario=venditore).select_related('mittente', 'asta__prodotto').values('mittente__username', 'valutazione', 'descrizione', 'asta__prodotto__nome','asta__id')
    media_valutazioni = recensioni.aggregate(media=Avg('valutazione'))['media']    
    # Crea un contesto per le aste attive con il prezzo corrente
    aste_attive_con_prezzo = []
    for asta in aste_attive:
        highest_bid = asta.offerte.order_by('-valore_offerta').first()
        if highest_bid:
            prezzo_corrente = highest_bid.valore_offerta
        else:
            prezzo_corrente = asta.prezzo_di_partenza
        aste_attive_con_prezzo.append({'asta': asta, 'prezzo_corrente': prezzo_corrente})

    # Ottieni le aste concluse del venditore
    aste_concluse = Asta.objects.filter(venditore=venditore, is_active=False)
    
    # Crea un contesto per le aste concluse con il prezzo più alto
    aste_concluse_con_prezzo = []
    for asta in aste_concluse:
        highest_bid = asta.offerte.order_by('-valore_offerta').first()
        if highest_bid:
            prezzo_corrente = highest_bid.valore_offerta
        else:
            prezzo_corrente = asta.prezzo_di_partenza
        aste_concluse_con_prezzo.append({'asta': asta, 'prezzo_corrente': prezzo_corrente})

    # Passa le aste attive e concluse al template
    context = {
        'venditore': venditore,
        'aste_attive_con_prezzo': aste_attive_con_prezzo,
        'aste_concluse_con_prezzo': aste_concluse_con_prezzo,
        'recensioni': list(recensioni),  
        'media_valutazioni':media_valutazioni,
    }

    return render(request, 'visualizza_venditore.html', context)

@login_required
def asta_conclusa(request, asta_id):
    asta = get_object_or_404(Asta, pk=asta_id)

    if asta.is_active:
        raise PermissionDenied("L'asta non è ancora conclusa.")

    highest_bid = asta.offerte.order_by('-valore_offerta').first()
    highest_bidder = highest_bid.profilo if highest_bid else None

    can_review = request.user == asta.venditore or request.user == highest_bidder

    existing_review = None
    if can_review:
        destinatario = asta.venditore if request.user == highest_bidder else highest_bidder
        existing_review = Recensione.objects.filter(mittente=request.user, destinatario=destinatario, asta=asta).first()

    if request.method == 'POST' and can_review and not existing_review:
        form = RecensioneForm(request.POST)
        if form.is_valid():
            recensione = form.save(commit=False)
            recensione.mittente = request.user
            recensione.destinatario = destinatario
            recensione.asta = asta
            recensione.save()
            messages.success(request, "Recensione inviata con successo.")
            return redirect('asta:asta_conclusa', asta_id=asta.id)
    else:
        form = RecensioneForm() if can_review and not existing_review else None

    existing_reviews = Recensione.objects.filter(asta=asta)

    # Se l'asta si è conclusa senza offerte e l'utente è il venditore
    if not highest_bid and request.user == asta.venditore:
        if request.method == 'POST' :
            new_asta_form = AstaForm(request.POST)
            if new_asta_form.is_valid():
                nuova_asta = new_asta_form.save(commit=False)
                nuova_asta.prodotto = asta.prodotto
                nuova_asta.venditore = request.user
                nuova_asta.start_time = timezone.now()
                nuova_asta.save()
                asta.delete()
                messages.success(request, "Il prodotto è stato rimesso all'asta con successo.")
                return redirect('home')
        else:
            new_asta_form = AstaForm()
    else:
        new_asta_form = None

    context = {
        'asta': asta,
        'highest_bid': highest_bid.valore_offerta if highest_bid else asta.prezzo_di_partenza,
        'highest_bidder': highest_bidder,
        'can_review': can_review,
        'form': form,
        'existing_review': existing_review,
        'existing_reviews': existing_reviews,
        'new_asta_form': new_asta_form,  # Passa il form per la nuova asta al template
    }
    return render(request, 'asta_conclusa.html', context)


def suggestions(request):
    query = request.GET.get('q', '')
    if query:
        aste = Asta.objects.filter(prodotto__nome__icontains=query)[:5]
        suggestions = list(aste.values('prodotto__nome'))
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)





from django.http import JsonResponse

def countdown(request, asta_id):
    asta = get_object_or_404(Asta, pk=asta_id)
    highest_bid = asta.offerte.order_by('-valore_offerta').first()
    is_asta_scaduta = asta.end_time <= timezone.now() or not asta.is_active

    highest_bidder = highest_bid.profilo if highest_bid else None
    is_highest_bidder = request.user == highest_bidder if request.user.is_authenticated else False

    now = timezone.now()
    is_time_remaining = False
    formatted_end_time = asta.end_time.strftime("%d/%m/%Y %H:%M")

    if asta.end_time.date() == now.date():
        time_remaining = asta.end_time - now
        formatted_end_time = "{:02d}:{:02d}:{:02d}".format(time_remaining.seconds // 3600, (time_remaining.seconds // 60) % 60, time_remaining.seconds % 60)
        is_time_remaining = True

    data = {
        'formatted_end_time': formatted_end_time,
        'is_asta_scaduta': is_asta_scaduta,
    }

    return JsonResponse(data)
