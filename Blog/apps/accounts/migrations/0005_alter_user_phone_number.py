# Generated by Django 3.2 on 2022-02-10 12:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220210_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, help_text='The phone number must be in the format: "+380999999999"', max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='The phone number must be in the format: "+380999999999". Starts with "+380" and 9 digits.', regex='^\\+380\\d{9}')], verbose_name='phone number'),
        ),
    ]
