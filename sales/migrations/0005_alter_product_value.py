# Generated by Django 3.2.8 on 2021-10-16 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_alter_product_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
