# Generated by Django 3.2.6 on 2021-08-25 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0010_studentnotetype_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='absence_acceptance',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='absence',
            name='absence_reason',
            field=models.CharField(default='', max_length=225),
        ),
        migrations.AlterField(
            model_name='absence',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='grade.student'),
            preserve_default=False,
        ),
    ]
