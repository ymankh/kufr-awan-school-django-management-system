# Generated by Django 3.2.6 on 2021-08-17 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='student',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
