# Generated by Django 5.1.2 on 2024-11-02 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_cart_updated_at_cart_session_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]