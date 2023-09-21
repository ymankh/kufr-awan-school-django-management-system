# Generated by Django 4.2.4 on 2023-09-16 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0003_skilloption_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade.skill')),
                ('skill_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade.skilloption')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade.student')),
            ],
        ),
    ]