# Generated by Django 4.0.2 on 2022-02-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_profile_n_algo_coin_alter_profile_algo_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ALGO_Wallet',
            field=models.FloatField(default=1.88837),
        ),
        migrations.AlterField(
            model_name='profile',
            name='USD_wallet',
            field=models.FloatField(default=10001),
        ),
    ]
