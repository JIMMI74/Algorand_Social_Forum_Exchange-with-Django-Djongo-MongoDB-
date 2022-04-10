# Generated by Django 4.0.2 on 2022-03-11 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordertransaction', '0003_remove_order_name_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_order_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
