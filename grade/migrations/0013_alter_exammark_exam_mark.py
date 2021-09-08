# Generated by Django 3.2.7 on 2021-09-04 17:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0012_auto_20210904_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exammark',
            name='exam_mark',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]