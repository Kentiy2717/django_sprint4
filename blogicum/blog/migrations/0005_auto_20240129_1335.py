# Generated by Django 3.2.16 on 2024-01-29 06:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20240129_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания'),
        ),
    ]
