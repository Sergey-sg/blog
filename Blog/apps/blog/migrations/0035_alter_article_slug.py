# Generated by Django 3.2 on 2022-02-16 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0034_alter_imagearticle_image_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, help_text='used to generate URL', null=True),
        ),
    ]