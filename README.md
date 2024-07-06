# DjangoBid

DjangoBid è una piattaforma di aste online sviluppata con Django.

## Istruzioni per Avviare il Progetto Django

1. **Creare e attivare un virtual environment:**

    ```bash
    pipenv shell
    ```
    

2. **Avviare il server di sviluppo:**

    ```bash
    python manage.py runserver
    ```

    Il progetto sarà accessibile all'indirizzo `http://127.0.0.1:8000/`.

## Istruzioni per Avviare i Test Django

1. **Assicurarsi che il virtual environment sia attivo.**
2. **Eseguire i test:**

    ```bash
    python manage.py test 
    ```
    Questo comando eseguirà tutti i test presenti nel progetto.
    
    Altrimenti, per eseguire i 2 test in modo separato:
    
    ```bash
    python manage.py test  utente.tests
    ```
    ```bash
    python manage.py test asta.tests
    ```

## Librerie e Software Utilizzati

- **Django**
- **JQuery**
- **Ajax**
- **Bootstrap5.3**
- **Json**
- **Os**
- **django-crispy-forms**



