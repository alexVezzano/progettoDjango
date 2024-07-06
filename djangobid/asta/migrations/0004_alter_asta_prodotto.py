# Generated by Django 5.0.6 on 2024-06-25 07:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asta', '0003_alter_recensione_asta_and_more'),
        ('prodotto', '0004_alter_prodotto_immagine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asta',
            name='prodotto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aste', to='prodotto.prodotto'),
        ),
    ]