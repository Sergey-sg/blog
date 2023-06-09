# Generated by Django 3.2 on 2022-02-10 11:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_subscription'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['email'], 'verbose_name': 'user', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='used to login the site', max_length=254, unique=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='img_alt',
            field=models.CharField(blank=True, help_text='text to be loaded in case of image loss', max_length=200, null=True, verbose_name='image alternative'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, help_text='The phone number must be in the format: "+380999999999"', max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть в формате: "+380999999999". Начинается из "+380" и 9 цифр.', regex='^\\+380\\d{9}')], verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, help_text='Profile photo', null=True, upload_to='user_photo/%Y/%m/%d', verbose_name='photo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='subscription',
            field=models.ManyToManyField(blank=True, help_text='author subscription', to=settings.AUTH_USER_MODEL, verbose_name='subscription'),
        ),
    ]
