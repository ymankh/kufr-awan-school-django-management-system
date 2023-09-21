from django.contrib import admin
from grade.models import *

admin.site.site_title = "Yman admin page"
admin.site.site_header = "Kofer awan school system"


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ("student", "absence_date", "grade", "section")
    list_filter = ("student", "absence_date", "student__grade", "student__section")


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ExamMark)
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


@admin.register(StudentNoteType)
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


@admin.register(ParticipationOption)
class ParticipationOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("group",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "grade")


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectModel)
class SubjectModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model')


@admin.register(SkillOption)
class SkillOptionAdmin(admin.ModelAdmin):
    pass

@admin.register(SkillNote)
class SkillNoteAdmin(admin.ModelAdmin):
    list_display = ("student", "skill", "skill_option", "grade")
    list_editable = ("skill_option",)
    def grade(self, obj):
        return obj.student.grade