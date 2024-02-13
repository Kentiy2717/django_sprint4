# Generated by Django 3.2.16 on 2024-01-29 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикуется')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('title', models.CharField(help_text='Не более 256 символов', max_length=256, verbose_name='Название категории')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Тематическая категория',
                'ordering': ('title', 'is_published'),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикуется')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('name', models.CharField(help_text='Не более 256 символов', max_length=256, verbose_name='Название локации')),
            ],
            options={
                'verbose_name': 'локация',
                'verbose_name_plural': 'Географическая метка',
                'ordering': ('name', 'is_published'),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикуется')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('title', models.CharField(help_text='Не более 256 символов', max_length=256, verbose_name='Заголовок поста')),
                ('text', models.TextField(verbose_name='Текст поста')),
                ('pub_date', models.DateTimeField(verbose_name='Время публикации')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category', verbose_name='Категория')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.location', verbose_name='Локация')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'Публикация',
                'ordering': ('title', 'is_published'),
            },
        ),
    ]
