# Generated by Django 3.2 on 2022-02-06 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_auto_20220206_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='recommended',
            field=models.ManyToManyField(to='blog.Article', verbose_name='рекомендованные статьи'),
        ),
    ]
