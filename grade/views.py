from random import shuffle
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, QuerySet
from django.shortcuts import get_object_or_404
from .models import (
    Student,
    StudentNote,
    Grade,
    Section,
    StudentNoteType,
    Group,
    Absence,
    ParticipationOption,
    Participation,
    Skill,
    SkillOption,
    SkillNote,
    SubjectModel,
    Subject,
)


def only_staff_message(
    request, message="you dont have the permission to Enter this page!!"
):
    messages.add_message(
        request,
        messages.WARNING,
        message=message,
    )
    return redirect("index")


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
def absence_table(request, grade_id, section_id, group_id):
    # make sure only staff can reach this page
    if not request.user.is_staff:
        return only_staff_message(request)

    if request.method == "POST":
        data = request.POST
        # take the id's of the students and set an absence on each one
        if data["absence"]:
            Absence.objects.bulk_create(
                [
                    Absence(student=Student(id=stu_id))
                    for stu_id in data.getlist("absence")
                ],
                ignore_conflicts=True,
            )
    if group_id == 0:
        students = (
            Student.objects.annotate(Count("absence"))
            .filter(grade=Grade(id=grade_id), section=Section(id=section_id))
            .order_by("full_name")
        )
    else:
        students = (
            Student.objects.annotate(Count("absence"))
            .filter(
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
        return only_staff_message(request)
    if request.GET:
        data = request.GET
        return redirect(data["page"], data["grade"], data["section"], data["group"])
    page_options = (
        ["students_table", "Absence"],
        ["participation_table", "Participation"],
        ["chose_skill", "Chose Skill"],
        ["chose_subject_for_skill_table", "Subject Skill Table"],
    )
    return render(
        request,
        "chose_grade.html",
        {
            "sections": Section.objects.all(),
            "grades": Grade.objects.all(),
            "groups": Group.objects.all(),
            "page_options": page_options,
        },
    )


# import csv
# def test(request):
#     with open('csv/7c.csv', 'r', encoding='utf-8') as file:
#         file = csv.reader(file)
#         i = 0
#         for line in file:
#             student = Student()
#             student.full_name = line[0]
#             start_at = "73000000"
#             if i >= 10:
#                 student.national_id = start_at + str(i)
#             else:
#                 student.national_id = start_at + "0" + str(i)
#             student.grade = Grade.objects.get(grade="السابع")
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
        return only_staff_message(request)
    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        data = request.POST
        # delete list of selected notes
        if "deleted_notes_list" in data:
            StudentNote.objects.filter(
                id__in=data.getlist("deleted_notes_list")
            ).delete()
        elif "absences" in data:
            Absence.objects.filter(id__in=data.getlist("absences")).delete()
        # add a written note to the student.
        elif "deleted_participations_list" in data:
            Participation.objects.filter(
                id__in=data.getlist("deleted_participations_list")
            ).delete()
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
    participations: QuerySet[Participation] = Participation.objects.select_related(
        "participation_option", "participation_option__note_type"
    ).filter(student=student)
    return render(
        request,
        "student_edit.html",
        {
            "student_id": student_id,
            "student": student,
            "note_types": StudentNoteType.objects.all(),
            "notes": StudentNote.objects.filter(student=student),
            "absences": Absence.objects.filter(student=student),
            "participations": participations,
        },
    )


def participation_table(request, grade_id, section_id, group_id):
    if not request.user.is_staff:
        return only_staff_message(request)
    if request.method == "POST":
        data = request.POST
        participation = data.getlist("participations")
        notes = []
        for p in participation:
            student, participation_option = p.split(",")
            notes += [
                Participation(
                    student_id=student, participation_option_id=participation_option
                )
            ]
        Participation.objects.bulk_create(notes)
        return redirect(
            participation_table,
            grade_id=grade_id,
            section_id=section_id,
            group_id=group_id,
        )
    grade = Grade.objects.get(id=grade_id)
    section = Section.objects.get(id=section_id)
    if group_id != 0:
        group = Group.objects.get(id=group_id)
        students = Student.objects.annotate(p_count=Count("participation")).filter(
            group=group, grade=grade, section=section
        )
    else:
        students = Student.objects.annotate(p_count=Count("participation")).filter(
            grade=grade, section=section
        )
    participation_options = ParticipationOption.objects.all()
    students = list(students)
    shuffle(students)
    return render(
        request,
        "participation_table.html",
        context={
            "students": students,
            "participation_options": participation_options,
            "grade": grade,
            "section": section,
        },
    )


def skills_table(request, grade_id, section_id, group_id, skill_id):
    if not request.user.is_staff:
        return only_staff_message(request)
    grade = get_object_or_404(Grade, id=grade_id)
    section = get_object_or_404(Section, id=section_id)
    if group_id != 0:
        group = Group.objects.get(id=group_id)
        students = Student.objects.filter(
            group=group, grade=grade, section=section
        ).values_list("id", "full_name")
    else:
        students = Student.objects.values_list("id", "full_name").filter(
            grade=grade, section=section
        )
    skill = get_object_or_404(Skill, id=skill_id)
    if request.method == "POST":
        data = request.POST
        skills = data.getlist("skills")
        notes = []
        for skill in skills:
            student_id, p_option = skill.split(",")
            obj, created = SkillNote.objects.get_or_create(
                student_id=student_id, skill_id=skill_id
            )
            if created:
                # If the object is created, set its value
                obj.skill_option_id = p_option
                notes.append(obj)
            else:
                obj.skill_option_id = p_option
                notes.append(obj)
        if notes:
            SkillNote.objects.bulk_update(notes, fields=["skill_option"])
        return redirect(
            "subject_skill_table",
            grade_id=grade_id,
            section_id=section_id,
            group_id=group_id,
            subject_id=Skill.objects.get(id=skill_id).model.subject.pk,
        )
    skill_options = SkillOption.objects.all()
    students_with_notes_ids = [student[0] for student in students]
    skill_notes = SkillNote.objects.values_list("student_id", "skill_option_id").filter(
        student_id__in=students_with_notes_ids, skill=skill
    )
    table = []
    skill_student_ids = [skill_note[0] for skill_note in skill_notes]
    for student in students:
        row = [student, -1]
        # get the option of the id of the skill option if exist
        if student[0] in skill_student_ids:
            row[1] = skill_notes[skill_student_ids.index(student[0])][1]
        table.append(row)
    print(skill_student_ids)

    return render(
        request,
        "skill.html",
        context={
            "table": table,
            "participation_options": skill_options,
            "grade": grade,
            "section": section,
            "skill": skill,
        },
    )


def chose_skill(request, grade_id, section_id, group_id):
    if not request.user.is_staff:
        return only_staff_message(request)
    if request.method == "POST":
        data = request.POST
        if "subject" in data:
            subject = data["subject"]
            models = SubjectModel.objects.filter(subject_id=subject)
            skills = ((model, Skill.objects.filter(model=model)) for model in models)
            return render(request, "chose_skill.html", {"skills": skills})
        if "skill" in data:
            return redirect(skills_table, grade_id, section_id, group_id, data["skill"])
    subjects = Subject.objects.filter(grade_id=grade_id)
    return render(request, "chose_skill.html", {"subjects": subjects})


def subject_skill_table(request, grade_id, section_id, group_id, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    grade = get_object_or_404(Grade, id=grade_id)
    section = get_object_or_404(Section, id=section_id)
    students = Student.objects.values_list("id", "full_name").filter(
        grade_id=grade_id, section_id=section_id
    )
    students_ids = [student[0] for student in students]
    models = SubjectModel.objects.filter(subject_id=subject_id).values_list(
        "id", "name"
    )
    skills = [
        Skill.objects.values_list("id", "name").filter(model_id=model[0])
        for model in models
    ]
    if not skills:
        return only_staff_message(request, "There are no skills registered yet!!!")
    # to get the number of column for each model.
    model_skill_counts = [len(model_skills) for model_skills in skills]
    # Make the skill set flat.
    skills = [x for y in skills for x in y]
    skills_notes = SkillNote.objects.values_list(
        "skill_id", "student_id", "skill_option__name"
    ).filter(student_id__in=students_ids)

    students_with_notes_ids = [skill_note[1] for skill_note in skills_notes]
    num_of_skills = sum(model_skill_counts)
    table = []
    skills_ids = [skill[0] for skill in skills]
    for student in students:
        row = [
            "____",
        ] * (num_of_skills + 1)
        row[0] = student[1]
        if student[0] in students_with_notes_ids:
            student_notes = [skill_note for skill_note in skills_notes if skill_note[1]==student[0]]
            for skill_note in student_notes:
                row[skills_ids.index(skill_note[0]) + 1] = skill_note[2]
        table.append(row)
    return render(
        request,
        "subject_skill_table.html",
        context={
            "table": table,
            "models": zip(models, model_skill_counts),
            "skills": skills,
            "subject": subject,
            "grade": grade,
            "section": section,
            "group_id": group_id,
        },
    )


def chose_subject_for_skill_table(request, grade_id, section_id, group_id):
    if not request.user.is_staff:
        return only_staff_message(request)
    if request.method == "POST":
        data = request.POST
        if "subject" in data:
            return redirect(
                "subject_skill_table", grade_id, section_id, group_id, data["subject"]
            )
    subjects = Subject.objects.filter(grade_id=grade_id)
    return render(request, "chose_skill.html", {"subjects": subjects})
