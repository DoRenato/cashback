# Generated by Django 3.2.8 on 2021-10-17 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0019_alter_product_product_type2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type', to='sales.producttype', verbose_name='type'),
        ),
    ]
