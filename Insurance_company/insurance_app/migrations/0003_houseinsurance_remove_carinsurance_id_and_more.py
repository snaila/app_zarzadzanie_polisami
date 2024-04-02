# Generated by Django 5.0.2 on 2024-03-30 11:14

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0002_carinsurance_price_carinsurance_valid_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='HouseInsurance',
            fields=[
                ('policy_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('policy_name', models.CharField(max_length=100, unique=True)),
                ('policy_description', models.TextField(max_length=2000)),
                ('valid_to', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('house_type', models.CharField(choices=[(1, 'Dom'), (2, 'Szeregowiec'), (3, 'Mieszkanie')], max_length=100)),
                ('number_of_owners', models.PositiveSmallIntegerField(default=1)),
                ('house_area', models.PositiveIntegerField()),
                ('house_city', models.CharField(max_length=50)),
                ('house_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
            ],
        ),
        migrations.RemoveField(
            model_name='carinsurance',
            name='id',
        ),
        migrations.AddField(
            model_name='carinsurance',
            name='policy_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='carinsurance',
            name='policy_name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='carinsurance',
            name='valid_to',
            field=models.DateField(),
        ),
    ]