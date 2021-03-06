# Generated by Django 3.2.8 on 2021-10-29 19:28

import account.enums
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('exchange', models.CharField(choices=[('coinex', account.enums.ExchangeEnum['COINEX']), ('kucoin', account.enums.ExchangeEnum['KUCOIN'])], default='coinex', max_length=32)),
                ('access_id', models.CharField(max_length=128)),
                ('secret_key', models.CharField(max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'info',
            },
        ),
        migrations.AddConstraint(
            model_name='info',
            constraint=models.UniqueConstraint(fields=('user', 'exchange'), name='unique_user_exchange'),
        ),
    ]
