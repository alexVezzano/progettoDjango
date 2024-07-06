# Generated by Django 5.0.6 on 2024-06-29 20:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asta', '0004_alter_asta_prodotto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asta',
            name='prezzo_di_partenza',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]
