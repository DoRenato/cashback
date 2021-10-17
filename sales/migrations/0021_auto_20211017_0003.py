# Generated by Django 3.2.8 on 2021-10-17 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0020_alter_product_product_type2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_type2',
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.producttype'),
        ),
    ]
