# Generated by Django 5.0.2 on 2024-04-13 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0014_carpolicyfactors'),
    ]

    operations = [
        migrations.CreateModel(
            name='HousePolicyFactors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]