# Generated by Django 4.2.3 on 2023-08-04 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_favourites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='products',
            new_name='product',
        ),
    ]
