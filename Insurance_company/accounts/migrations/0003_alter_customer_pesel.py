# Generated by Django 5.0.2 on 2024-04-11 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customer_first_name_remove_customer_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='pesel',
            field=models.CharField(max_length=11),
        ),
    ]