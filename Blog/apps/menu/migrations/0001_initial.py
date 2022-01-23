# Generated by Django 3.2 on 2022-01-23 17:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('dd_order', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('item_url', models.CharField(help_text='Enter link address', max_length=2048, unique=True, validators=[django.core.validators.RegexValidator(message='If the link is internal it should look like this: "blog/article/", for external links it should look like this: "https://site.com/"', regex='^((http(s)?:\\/\\/)?([\\w-]+\\.?)+[\\w-]+[.com]+([\\w\\-\\.,@?^=%&amp;:/~\\+#]*[\\w\\-\\@?^=%&amp;/~\\+#])?)')])),
                ('target', models.CharField(choices=[('b', '_blank'), ('s', '_self')], default='s', help_text='Target url', max_length=1)),
                ('position', models.CharField(choices=[('h', 'header'), ('f', 'footer')], help_text='Position object (header or footer)', max_length=1)),
                ('show_item', models.BooleanField(default=False, verbose_name='show')),
            ],
            options={
                'verbose_name': 'menu item',
                'verbose_name_plural': 'Menu items',
                'ordering': ['dd_order', 'created'],
            },
        ),
    ]
