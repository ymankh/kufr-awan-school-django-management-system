from django.contrib import admin
from grade.models import *

admin.site.site_title = "Yman admin page"
admin.site.site_header = "Kofer awan school system"


class SectionAdmin(admin.ModelAdmin):
    pass


class GradeAdmin(admin.ModelAdmin):
    pass


class AbsenceAdmin(admin.ModelAdmin):
    list_display = ("student", "absence_date", "grade", "section")
    list_filter = ("student", "absence_date", "student__grade", "student__section")


class ExamTypeAdmin(admin.ModelAdmin):
    pass


class ExamMarkAdmin(admin.ModelAdmin):
    list_display = ("student",)


class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "grade", "section")
    list_filter = ("full_name", "grade", "section")
    list_select_related = True


class StudentNoteTypeAdmin(admin.ModelAdmin):
    pass


class StudentNoteAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


class PhoneAdmin(admin.ModelAdmin):
    pass


admin.site.register(Section, SectionAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Absence, AbsenceAdmin)
admin.site.register(ExamType, ExamTypeAdmin)
admin.site.register(ExamMark, ExamMarkAdmin)
admin.site.register(StudentNoteType, StudentNoteTypeAdmin)
admin.site.register(StudentNote, StudentNoteTypeAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Phone, PhoneAdmin)
