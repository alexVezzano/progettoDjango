from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from asta.models import Asta, Offerta
from django.urls import reverse
from django.contrib import messages

class UpdateStatoAste:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = timezone.now()

        # Controllare le aste scadute
        aste_scadute = Asta.objects.filter(end_time__lt=now, is_active=True)

        if aste_scadute.exists():
            for asta in aste_scadute:
                asta.is_active = False
                asta.save()

                # offerente più alto
                highest_bid = asta.offerte.order_by('-valore_offerta').first()

                if highest_bid:
                    asta_url = request.build_absolute_uri(reverse('asta:asta_conclusa', kwargs={'asta_id': asta.id}))

                    # Render email per offerente più alto
                    email_content_bidder = render_to_string('emails/asta_vinta.html', {
                        'highest_bidder': highest_bid.profilo,
                        'asta': asta,
                        'highest_bid': highest_bid,
                        'asta_url': asta_url,
                    })

                    # Invio mail all'offerente più alto
                    send_mail(
                        'Asta Conclusa - Hai Vinto!',
                        email_content_bidder,
                        'no-reply@asta.com',
                        [highest_bid.profilo.email],
                        fail_silently=False,
                    )

                    # Render email per venditore
                    email_content_seller = render_to_string('emails/asta_conclusa_venditore.html', {
                        'venditore': asta.venditore,
                        'asta': asta,
                        'highest_bid': highest_bid,
                        'highest_bidder': highest_bid.profilo,
                        'asta_url': asta_url,
                    })

                    # Invio mail al venditore
                    send_mail(
                        'Asta Conclusa - Prodotto Venduto',
                        email_content_seller,
                        'no-reply@asta.com',
                        [asta.venditore.email],
                        fail_silently=False,
                    )
                    #messaggi nella pagina per notificare le mail
                    if request.user == highest_bid.profilo:
                        messages.info(request, 'Congratulazioni! Hai vinto un\'asta. Controlla la tua email per ulteriori dettagli.')
                    if request.user == asta.venditore:
                        messages.info(request, 'Il tuo prodotto è stato venduto! Controlla la tua email per ulteriori dettagli.')
                else:
                    asta_url = request.build_absolute_uri(reverse('asta:asta_conclusa', kwargs={'asta_id': asta.id}))

                    # Render email venditore che non  riceve offerte
                    email_content = render_to_string('emails/asta_senza_offerte.html', {
                        'venditore': asta.venditore,
                        'asta': asta,
                        'asta_url': asta_url,
                    })

                    # Invia email solo al venditore
                    send_mail(
                        'Asta Conclusa - Nessuna Offerta',
                        email_content,
                        'no-reply@asta.com',
                        [asta.venditore.email],
                        fail_silently=False,
                    )

                    if request.user == asta.venditore:
                        messages.info(request, 'La tua asta è conclusa ma non ci sono state offerte. Controlla la tua email per ulteriori dettagli.')

        response = self.get_response(request)
        return response
