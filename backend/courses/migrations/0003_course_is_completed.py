# Generated by Django 4.2.1 on 2023-12-08 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_course_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
