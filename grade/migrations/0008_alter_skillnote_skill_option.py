# Generated by Django 4.2.4 on 2023-09-25 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0007_alter_skilloption_options_skilloption_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillnote',
            name='skill_option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='grade.skilloption'),
        ),
    ]
