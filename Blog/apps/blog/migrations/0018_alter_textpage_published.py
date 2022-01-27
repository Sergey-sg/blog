# Generated by Django 3.2 on 2022-01-27 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20220128_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textpage',
            name='published',
            field=models.CharField(choices=[('d', 'draft'), ('p', 'published')], default='d', help_text='Published or draft', max_length=1),
        ),
    ]
