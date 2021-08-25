# Generated by Django 3.2.6 on 2021-08-17 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExamType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_type', models.CharField(max_length=100)),
                ('exam_top_mark', models.IntegerField()),
                ('exam_pass_mark', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=10)),
                ('profile_pic', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('grade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='grade.grade')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='grade.section')),
            ],
        ),
        migrations.CreateModel(
            name='StudentNoteType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NoteType', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StudentNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=500)),
                ('note_date', models.DateField(auto_now=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='grade.student')),
            ],
        ),
        migrations.CreateModel(
            name='ExamMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='grade.examtype')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='grade.student')),
            ],
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absence_date', models.DateField(auto_now=True)),
                ('absence_reason', models.CharField(max_length=225)),
                ('absence_acceptance', models.BooleanField()),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='grade.student')),
            ],
        ),
    ]
