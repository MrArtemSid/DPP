# Generated by Django 5.0.5 on 2024-05-09 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0009_rename_id_item_sells_item_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sells',
            old_name='Item',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='sells',
            old_name='Seller',
            new_name='seller',
        ),
        migrations.RenameField(
            model_name='sells',
            old_name='Storage',
            new_name='storage',
        ),
        migrations.AlterField(
            model_name='seller',
            name='id_storage',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Store.storage'),
        ),
    ]