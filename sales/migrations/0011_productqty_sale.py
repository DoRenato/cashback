# Generated by Django 3.2.8 on 2021-10-16 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0010_remove_productqty_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='productqty',
            name='sale',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='sales.sale'),
            preserve_default=False,
        ),
    ]
