from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Model
from django.db.models.signals import post_delete
from django.dispatch import receiver


def validate_digit_length(phone):
    if not (phone.isdigit() and len(phone) == 10):
        raise ValueError('%(phone)s must be 10 digits')


class Section(models.Model):
    section = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.section


class Grade(models.Model):
    grade = models.CharField(max_length=10)

    def __str__(self):
        return self.grade


class Address(models.Model):
    governorate = models.CharField(max_length=30, default="Irbid")
    district = models.CharField(max_length=30, default="Al-Kourah")
    neighborhood = models.CharField(max_length=30, default="KufrAwan")


class Phone(models.Model):
    phone = models.CharField(max_length=10, validators=[validate_digit_length], unique=True)

    def __str__(self):
        return self.phone


class Group(models.Model):
    group = models.CharField(max_length=1, unique=True)

    def __str__(self):
        return self.group


class Student(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    national_id = models.CharField(verbose_name="national id", max_length=10,
                                   validators=[validate_digit_length], unique=True, null=True)
    grade = models.ForeignKey(Grade, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL, blank=True)
    profile_pic = models.FileField(null=True, blank=True)
    mobile = models.OneToOneField(Phone, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def absence_count(self):
        return len(Absence.objects.filter(student=self))

    def __str__(self):
        return self.full_name

    # create user for each student
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

    def delete(self, using=None, keep_parents=False):
        user = User.objects.get(username=self.national_id)
        user.delete()
        print("del")
        super(Student, self).delete()


@receiver(post_delete, sender=Student)
def signal_function_name(sender, instance, using, **kwargs):
    user = User.objects.get(username=instance.national_id)
    user.delete()


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
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    top_mark = 100
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    exam_mark = models.IntegerField(validators=[MaxValueValidator(top_mark), MinValueValidator(0)], default=0)

    @property
    def exam_result(self):
        if self.exam_type.exam_pass_mark > self.exam_mark:
            return "fail"
        else:
            return "pass"

    def save(self, *args, **kwargs):
        self.top_mark = self.exam_type.exam_top_mark
        if self.exam_mark > self.top_mark:
            self.exam_mark = self.top_mark

        super(ExamMark, self).save(*args, **kwargs)

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

    @property
    def grade(self):
        return self.student.grade.grade

    @property
    def section(self):
        return self.student.section.section

    def __str__(self):
        return self.student.full_name + " " + self.note[0:100]
