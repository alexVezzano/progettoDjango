# Generated by Django 5.0.6 on 2024-06-15 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prodotto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descrizione', models.TextField()),
                ('categoria', models.CharField(choices=[('Elettronica', 'Elettronica'), ('Casa', 'Casa'), ('Moda', 'Moda')], max_length=50)),
                ('immagine', models.ImageField(upload_to='prodotti/')),
            ],
        ),
    ]