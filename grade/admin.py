from django.contrib import admin
from grade.models import *

admin.site.site_title = "Yman admin page"
admin.site.site_header = "Kofer awan school system"


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass


class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ("student", "absence_date", "grade", "section")
    list_filter = ("student", "absence_date", "student__grade", "student__section")


class ExamTypeAdmin(admin.ModelAdmin):
    pass


class ExamMarkAdmin(admin.ModelAdmin):
    list_display = ("student",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "grade", "group", "section")
    list_filter = ("grade", "section", "group")
    search_fields = ("full_name",)
    list_editable = (
        "section",
        "group",
    )


class StudentNoteTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentNote)
class StudentNoteAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "grade",
        "section",
        "note_type",
        "note",
    )
    search_fields = ("student__full_name", "note")
    list_editable = ("note", "note_type")
    list_filter = ("student__grade", "student__section")


class ParticipationOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


# @admin.register(Phone)
# class PhoneAdmin(admin.ModelAdmin):
#     pass


class GroupAdmin(admin.ModelAdmin):
    list_display = ("group",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "grade")


class HomeWorkAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectModel)
class SubjectModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass

# @admin.register(SkillOption)
class skillOptionAdmin(admin.ModelAdmin):
    pass