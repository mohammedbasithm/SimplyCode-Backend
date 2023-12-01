# Generated by Django 4.2.1 on 2023-11-29 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0004_customuser_teacher_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='certificate',
            field=models.ImageField(blank=True, null=True, upload_to='media/teacher_certificate/'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id_proof',
            field=models.ImageField(blank=True, null=True, upload_to='media/teacher_idproof/'),
        ),
    ]
