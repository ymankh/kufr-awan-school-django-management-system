from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import Student, StudentNote, Grade, Section, Absence
from django.utils import timezone
import json


def validate_digit_length(national_id):
    return national_id.isdigit() and len(national_id) == 10


def index(request):
    return render(request, "index.html")


# authentication

def logout_(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


def login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST['NationalID']
        if not validate_digit_length(username):
            messages.add_message(request, messages.WARNING, 'National ID should be a 10 digit number.')
            return redirect('login')
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect("index")
        else:
            messages.add_message(request, messages.WARNING, "Wrong National ID or Password")
        return redirect("login")

    return render(request, "login.html")


def profile(request):
    national_id = request.user.username
    student = Student.objects.get(national_id=national_id)
    notes = StudentNote.objects.filter(student=student)
    return render(request, "profile.html", {"notes": notes, "time_now": timezone.now()})


def students_table(request, grade_id, section_id):
    if request.method == "POST":
        # take the ideas of the students and set an absence on each one
        for stu_id in request.POST["students_absence"].split(","):
            Absence(student=Student(id=stu_id)).save()
    students = Student.objects.filter(grade=Grade(id=grade_id), section=Section(id=section_id))
    students_id = json.dumps([student.id for student in students])
    return render(request, "students_table.html",
                  {"grade_id": grade_id, "section_id": section_id, "students": students, "students_id": students_id})


def chose_grade(request):
    if request.GET:
        data = request.GET
        return redirect("students_table", data["grade"], data["section"])
    return render(request, "chose_grade.html", {"sections": Section.objects.all(),
                                                "grades": Grade.objects.all()})
