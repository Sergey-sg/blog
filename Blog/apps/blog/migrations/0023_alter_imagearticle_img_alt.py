# Generated by Django 3.2 on 2022-02-02 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20220131_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagearticle',
            name='img_alt',
            field=models.CharField(blank=True, help_text='текст, который будет загружен в случае потери изображения', max_length=200),
        ),
    ]
