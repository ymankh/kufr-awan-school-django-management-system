from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from .models import (
    Student,
    StudentNote,
    Grade,
    Section,
    Absence,
    StudentNoteType,
    Group,
    Absence,
)


def validate_digit_length(national_id):
    return national_id.isdigit() and len(national_id) == 10


def index(request):
    return render(request, "index.html")


# authentication


def logout_(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")


def login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST["NationalID"]
        if not validate_digit_length(username):
            messages.add_message(
                request, messages.WARNING, "National ID should be a 10 digit number."
            )
            return redirect("login")
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect("index")
        else:
            messages.add_message(
                request, messages.WARNING, "Wrong National ID or Password"
            )
        return redirect("login")

    return render(request, "login.html")


def profile(request):
    if not Student.objects.filter(national_id=request.user.username).exists():
        return redirect("index")
    national_id = request.user.username
    student = Student.objects.get(national_id=national_id)
    notes = StudentNote.objects.filter(student=student)
    return render(
        request,
        "profile.html",
        {"notes": notes, "time_now": timezone.now(), "student": student},
    )


# student tables
def students_table(request, grade_id, section_id, group_id):
    # make sure only staff can reach this page
    if not request.user.is_staff:
        return redirect("index")

    if request.method == "POST":
        data = request.POST
        # take the id's of the students and set an absence on each one
        if data["absence"]:
            Absence.objects.bulk_create(
                [
                    Absence(student=Student(id=stu_id))
                    for stu_id in data.getlist("absence")
                ]
            )
    if group_id == 0:
        students = (
            Student.objects.annotate(Count("absence")).filter(
                grade=Grade(id=grade_id), section=Section(id=section_id)
            ).order_by("full_name")
        )
    else:
        students = (
            Student.objects.annotate(Count("absence")).filter(
                grade=Grade(id=grade_id),
                section=Section(id=section_id),
                group=Group(id=group_id),
            )
            .order_by("full_name")
        )
    return render(
        request,
        "students_table.html",
        {"grade_id": grade_id, "section_id": section_id, "students": students},
    )


def chose_grade(request):
    if not request.user.is_staff:
        messages.add_message(
            request,
            messages.WARNING,
            message="you dont have the permission to Enter this page!!",
        )
        return redirect("index")
    if request.GET:
        data = request.GET
        return redirect("students_table", data["grade"], data["section"], data["group"])
    return render(
        request,
        "chose_grade.html",
        {
            "sections": Section.objects.all(),
            "grades": Grade.objects.all(),
            "groups": Group.objects.all(),
        },
    )


# import csv
#
#
# def test(request):
#     with open('csvs/fifth.csv', 'r', encoding='utf-8') as file:
#         file = csv.reader(file)
#         i = 0
#         for line in file:
#             student = Student()
#             student.full_name = line[0]
#             start_at = "63000000"
#             if i >= 10:
#                 student.national_id = start_at + str(i)
#             else:
#                 student.national_id = start_at + "0" + str(i)
#             student.grade = Grade.objects.get(grade="sixth")
#             student.section = Section.objects.get(section="ج")
#             try:
#                 student.save()
#             except:
#                 pass
#             i += 1
#     return redirect('index')


def edit_student_information(request, student_id):
    # Make sure only staff can reach this page.
    if not request.user.is_staff:
        redirect("index")

    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        data = request.POST
        # delete list of selected notes
        if "deleted_notes_list" in data and data["deleted_notes_list"]:
            StudentNote.objects.filter(
                id__in=data.getlist("deleted_notes_list")
            ).delete()
        elif "absences" in data and data["absences"]:
            Absence.objects.filter(id__in=data.getlist("absences")).delete()
        # add a written note to the student.
        elif "note_type" in data:
            # check for missing fields
            if not data.get("note_type"):
                messages.add_message(
                    request,
                    messages.WARNING,
                    message="You did note Specify the note type!",
                )
            elif not data.get("note_text", None):
                messages.add_message(
                    request,
                    messages.WARNING,
                    message="You did not enter the Note Text! ",
                )
            else:
                # save the note
                StudentNote(
                    student=student,
                    note_type=StudentNoteType(id=data["note_type"]),
                    note=data["note_text"],
                ).save()

        return redirect("student_information_edit", student_id=student_id)
    return render(
        request,
        "student_edit.html",
        {
            "student_id": student_id,
            "student": student,
            "note_types": StudentNoteType.objects.all(),
            "notes": StudentNote.objects.filter(student=student),
            "absences": Absence.objects.filter(student=student),
        },
    )
