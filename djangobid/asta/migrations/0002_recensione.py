# Generated by Django 5.0.6 on 2024-06-20 16:01

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asta', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recensione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valutazione', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('descrizione', models.TextField()),
                ('asta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='asta.asta')),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recensioni_ricevute', to=settings.AUTH_USER_MODEL)),
                ('mittente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recensioni_inviate', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
