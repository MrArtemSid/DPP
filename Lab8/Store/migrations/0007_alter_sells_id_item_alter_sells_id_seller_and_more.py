# Generated by Django 5.0.5 on 2024-05-09 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0006_alter_seller_id_storage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sells',
            name='id_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.item'),
        ),
        migrations.AlterField(
            model_name='sells',
            name='id_seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.seller'),
        ),
        migrations.AlterField(
            model_name='sells',
            name='id_storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.storage'),
        ),
    ]