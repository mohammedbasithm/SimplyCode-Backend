# Generated by Django 4.2.1 on 2023-12-27 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_chapter_is_free'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
