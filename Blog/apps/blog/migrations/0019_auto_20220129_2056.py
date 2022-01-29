# Generated by Django 3.2 on 2022-01-29 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_textpage_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='average_rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
        migrations.AddField(
            model_name='article',
            name='number_of_likes',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='number_of_reviews',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
