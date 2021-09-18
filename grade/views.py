from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import Student, StudentNote, Grade, Section, Absence, StudentNoteType, Group
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
    if not Student.objects.filter(national_id=request.user.username).exists():
        return redirect('index')
    national_id = request.user.username
    student = Student.objects.get(national_id=national_id)
    notes = StudentNote.objects.filter(student=student)
    return render(request, "profile.html", {"notes": notes, "time_now": timezone.now(), "student": student})


def students_table(request, grade_id, section_id, group_id):
    if not request.user.is_staff:
        return redirect("index")
    if request.method == "POST":
        # take the id's of the students and set an absence on each one
        if request.POST["students_absence"]:
            for stu_id in request.POST["students_absence"].split(","):
                Absence(student=Student(id=stu_id)).save()
    if group_id == 0:
        students = Student.objects.filter(grade=Grade(id=grade_id), section=Section(id=section_id))
    else:
        students = Student.objects.filter(grade=Grade(id=grade_id), section=Section(id=section_id),
                                          group=Group(id=group_id))
    students_id = json.dumps([student.id for student in students])
    return render(request, "students_table.html",
                  {"grade_id": grade_id, "section_id": section_id,
                   "students": students, "students_id": students_id})


def chose_grade(request):
    if not request.user.is_staff:
        messages.add_message(request, messages.WARNING, message="you dont have the permission to Enter this page!!")
        return redirect("index")
    if request.GET:
        data = request.GET
        return redirect("students_table", data["grade"], data["section"], data['group'])
    return render(request, "chose_grade.html", {
        "sections": Section.objects.all(),
        "grades": Grade.objects.all(),
        "groups": Group.objects.all(),
    })


# import csv
def test(request):
    # with open('static/students_list/6c.csv', 'r', encoding='utf-8') as file:
    #     file = csv.reader(file)
    #     i = 0
    #     for line in file:
    #         student = Student()
    #         student.full_name = line[1]
    #         if i >= 10:
    #             student.national_id = "63000000" + str(i)
    #         else:
    #             student.national_id = "630000000" + str(i)
    #         student.grade = Grade.objects.get(grade="سادس")
    #         student.section = Section.objects.get(section="ج A")
    #         try:
    #             student.save()
    #         except:
    #             pass
    #         i += 1
    return redirect('index')


def edit_student_information(request, student_id):
    if not request.user.is_staff:
        redirect("index")
    student = Student.objects.get(id=student_id)
    if request.method == "POST":
        data = request.POST
        # check for missing fields
        if not data.get("note_type"):
            messages.add_message(request, messages.WARNING, message="You did note Specify the note type!")
        elif not data.get("note_text", None):
            messages.add_message(request, messages.WARNING, message="You did not enter the Note Text! ")
        else:
            # save the note
            StudentNote(student=student, note_type=StudentNoteType(id=data["note_type"]), note=data["note_text"]).save()
    return render(request, "student_edit.html", {
        "student_id": student_id,
        "student": student,
        "note_types": StudentNoteType.objects.all(),
        "notes": StudentNote.objects.filter(student=student)})
