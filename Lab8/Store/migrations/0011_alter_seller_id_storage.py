# Generated by Django 5.0.5 on 2024-05-09 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0010_rename_item_sells_item_rename_seller_sells_seller_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='id_storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.storage'),
        ),
    ]
