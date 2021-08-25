# Generated by Django 3.2.6 on 2021-08-20 16:43

from django.db import migrations, models
import grade.models


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0005_alter_student_national_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='national_id',
            field=models.CharField(default='1234567890', max_length=10, null=True, unique=True, validators=[grade.models.validate_digit_length], verbose_name='Phone number'),
        ),
    ]
