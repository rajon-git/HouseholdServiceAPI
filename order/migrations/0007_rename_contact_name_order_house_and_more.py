# Generated by Django 5.1.2 on 2024-11-16 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_city_order_contact_name_order_house_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='contact_name',
            new_name='house',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='house_number',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='phone_number',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='road_number',
            new_name='road',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='ward_number',
            new_name='ward',
        ),
    ]