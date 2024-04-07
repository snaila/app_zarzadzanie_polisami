# Generated by Django 5.0.2 on 2024-04-07 10:00

import django.db.models.deletion
import insurance_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customer_first_name_remove_customer_last_name_and_more'),
        ('insurance_app', '0006_merge_20240407_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carinsurance',
            name='average_year_mileage',
            field=models.CharField(choices=[(1, 'Poniżej 5 tys. km'), (2, 'do 10 tys. km'), (3, 'do 20 tys. km'), (4, 'powyżej 20 tys. km')], max_length=100),
        ),
        migrations.AlterField(
            model_name='carinsurance',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer'),
        ),
        migrations.AlterField(
            model_name='carinsurance',
            name='policy_id',
            field=models.CharField(default=insurance_app.models.generate_id, editable=False, max_length=19, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='carinsurance',
            name='policy_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_app.carpolicytype'),
        ),
        migrations.AlterField(
            model_name='houseinsurance',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer'),
        ),
        migrations.AlterField(
            model_name='houseinsurance',
            name='policy_id',
            field=models.CharField(default=insurance_app.models.generate_id, editable=False, max_length=19, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='houseinsurance',
            name='policy_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_app.housepolicytype'),
        ),
    ]