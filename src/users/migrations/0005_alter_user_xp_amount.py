# Generated by Django 5.2.1 on 2025-06-05 17:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_xp_amount_alter_user_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='xp_amount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(600)]),
        ),
    ]
