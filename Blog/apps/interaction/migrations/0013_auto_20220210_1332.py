# Generated by Django 3.2 on 2022-02-10 11:32

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0031_auto_20220210_1332'),
        ('interaction', '0012_auto_20220203_2208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentarticle',
            options={'ordering': ['article', '-created'], 'verbose_name': 'comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterModelOptions(
            name='favoritesarticle',
            options={'ordering': ['article', 'subscriber', '-created'], 'verbose_name': 'favorite', 'verbose_name_plural': 'Favorites'},
        ),
        migrations.AlterField(
            model_name='commentarticle',
            name='article',
            field=models.ForeignKey(help_text='commented article', on_delete=django.db.models.deletion.CASCADE, to='blog.article', verbose_name='article'),
        ),
        migrations.AlterField(
            model_name='commentarticle',
            name='author',
            field=models.ForeignKey(help_text='author of comment', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='commentarticle',
            name='message',
            field=ckeditor.fields.RichTextField(help_text='message (comment) of article', validators=[django.core.validators.MinLengthValidator(3)], verbose_name='message'),
        ),
        migrations.AlterField(
            model_name='commentarticle',
            name='score',
            field=models.ForeignKey(help_text='assessment of the author of the commented article', null=True, on_delete=django.db.models.deletion.SET_NULL, to='interaction.score', verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='commentarticle',
            name='status',
            field=models.CharField(choices=[('p', 'published'), ('b', 'blocked')], default='p', help_text='status of comment', max_length=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='score',
            name='article',
            field=models.ForeignKey(help_text='author of score', on_delete=django.db.models.deletion.CASCADE, to='blog.article', verbose_name='article'),
        ),
        migrations.AlterField(
            model_name='score',
            name='author',
            field=models.ForeignKey(help_text='author of score', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.DecimalField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], decimal_places=0, default=1, help_text='assessment of the author of the article', max_digits=1, verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='score',
            name='status',
            field=models.CharField(choices=[('p', 'published'), ('b', 'blocked')], default='p', help_text='status of comment', max_length=1, verbose_name='status'),
        ),
    ]
