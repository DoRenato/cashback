# Generated by Django 3.2.8 on 2021-10-17 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0025_alter_cashback_sold_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashback',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, to='sales.Product'),
        ),
    ]
