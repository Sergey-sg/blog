# Generated by Django 3.2 on 2022-02-06 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_alter_article_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_preview',
            field=models.ImageField(help_text='article preview', upload_to='article_preview/%Y/%m/%d'),
        ),
    ]
