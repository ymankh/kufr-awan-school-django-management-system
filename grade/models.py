from django.db import models
from django.contrib.auth.models import User


def validate_digit_length(phone):
    if not (phone.isdigit() and len(phone) == 10):
        raise ValueError('%(phone)s must be 10 digits')


class Section(models.Model):
    section = models.CharField(max_length=10)

    def __str__(self):
        return self.section


class Grade(models.Model):
    grade = models.CharField(max_length=10)

    def __str__(self):
        return self.grade


class Student(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    national_id = models.CharField(verbose_name="national id", max_length=10,
                                   validators=[validate_digit_length], unique=True, null=True)
    grade = models.ForeignKey(Grade, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    profile_pic = models.FileField(null=True, blank=True)

    @property
    def absence_count(self):
        return len(Absence.objects.filter(student=self))

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if User.objects.filter(username=self.national_id):
            super().save(*args, **kwargs)
        else:
            user = User()
            user.username = self.national_id
            user.set_password(self.national_id)
            name = self.full_name.split(" ")
            user.first_name = name[0]
            user.last_name = name[-1]
            user.save()
            super().save(*args, **kwargs)


class Absence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    absence_date = models.DateField(auto_now=True)
    absence_reason = models.CharField(max_length=225, default="")
    absence_acceptance = models.BooleanField(default=False)

    @property
    def grade(self):
        return self.student.grade

    @property
    def section(self):
        return self.student.section

    def __str__(self):
        return self.student.full_name


class ExamType(models.Model):
    exam_type = models.CharField(max_length=100)
    exam_top_mark = models.IntegerField()
    exam_pass_mark = models.IntegerField()

    def __str__(self):
        return self.exam_type


class ExamMark(models.Model):
    exam_type = models.ForeignKey(ExamType, null=True, on_delete=models.SET_NULL)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.exam_type.exam_type + " " + self.student.full_name


class StudentNoteType(models.Model):
    TAGS_CHOICES = [
        ('primary', 'primary'),
        ('secondary', 'secondary'),
        ('success', 'success'),
        ('danger', 'danger'),
        ('warning', 'warning'),
        ('info', 'info')
    ]
    NoteType = models.CharField(max_length=50)
    tag = models.CharField(max_length=10, choices=TAGS_CHOICES, default="", null=True)

    def __str__(self):
        return self.NoteType


class StudentNote(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    note = models.CharField(max_length=500)
    note_type = models.ForeignKey(StudentNoteType, null=True, on_delete=models.SET_NULL)
    note_date = models.DateField(auto_now=True)
    visible_to_student = models.BooleanField(default=False)

    def __str__(self):
        return self.student.full_name + " " + self.note[0:100]
