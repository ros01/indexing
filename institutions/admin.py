from django.contrib import admin
from .models import *


# admin.site.register(MyStudentProfiles)

class StudentProfileAdmin(admin.ModelAdmin):
  list_display = ('id', 'student', 'institution', 'sex', 'dob', 'marital_status', 'nationality')
  list_display_links = ('id', 'student', 'institution', 'sex', 'marital_status')
  list_filter = ('student', 'institution', 'sex', 'marital_status')
  search_fields = ('student', 'institution', 'sex', 'marital_status')
  list_per_page = 25


admin.site.register(StudentProfile, StudentProfileAdmin)

class UtmeGradeAdmin(admin.ModelAdmin):
  list_display = ('examination_body','timestamp')
  list_display_links = ('examination_body', 'timestamp')
  list_filter = ('examination_body', 'timestamp')
  search_fields = ('examination_body', 'timestamp')
  list_per_page = 25


admin.site.register(UtmeGrade, UtmeGradeAdmin)


class GceAlevelsAdmin(admin.ModelAdmin):
  list_display = ('examination_body', 'timestamp')
  list_display_links = ('examination_body', 'timestamp')
  list_filter = ('examination_body', 'timestamp')
  search_fields = ('examination_body', 'timestamp')
  list_per_page = 25


admin.site.register(GceAlevels, GceAlevelsAdmin)


class DegreeResultsAdmin(admin.ModelAdmin):
  list_display = ('degree_type', 'course', 'course_grade', 'timestamp')
  list_display_links = ('degree_type', 'course', 'timestamp')
  list_filter = ('degree_type', 'course', 'timestamp')
  search_fields = ('degree_type', 'course', 'timestamp')
  list_per_page = 25


admin.site.register(DegreeResults, DegreeResultsAdmin)



class TransferGradeAdmin(admin.ModelAdmin):
  list_display = ('course', 'degree_type', 'timestamp')
  list_display_links = ('course', 'degree_type', 'timestamp')
  list_filter = ('course', 'degree_type', 'timestamp')
  search_fields = ('course', 'degree_type', 'timestamp')
  list_per_page = 25


admin.site.register(TransferGrade, TransferGradeAdmin)



class StudentIndexingAdmin(admin.ModelAdmin):
  list_display = ('student_profile', 'slug', 'academic_session', 'admission_type', 'indexing_status', 'verification_status', 'rejection_status', 'timestamp', 'updated')
  list_display_links = ('student_profile', 'academic_session', 'admission_type', 'indexing_status', 'timestamp')
  list_filter = ('student_profile', 'academic_session', 'admission_type', 'indexing_status', 'timestamp')
  search_fields = ('student_profile', 'academic_session', 'admission_type', 'indexing_status', 'timestamp')
  list_per_page = 25


admin.site.register(StudentIndexing, StudentIndexingAdmin)



class IndexingPaymentAdmin(admin.ModelAdmin):
  list_display = ('institution', 'student_profile', 'student_indexing', 'academic_session', 'payment_status', 'rrr_number', 'receipt_number', 'payment_amount')
  list_display_links = ('institution', 'academic_session', 'payment_status', 'rrr_number', 'receipt_number')
  list_filter = ('institution', 'academic_session', 'payment_status', 'rrr_number', 'receipt_number')
  search_fields = ('institution', 'academic_session', 'payment_status', 'rrr_number', 'receipt_number')
  list_per_page = 25


admin.site.register(IndexingPayment, IndexingPaymentAdmin)


# class IndexingPaymentInline(admin.TabularInline):
#   model = IndexingPayment

# class InstitutionPaymentAdmin(admin.ModelAdmin):
#   inlines = [
#     IndexingPaymentInline
#   ]
#   class Meta:
#     model: InstitutionPayment

# admin.site.register(InstitutionPayment, InstitutionPaymentAdmin)

class InstitutionPaymentAdmin(admin.ModelAdmin):
  list_display = ('institution', 'academic_session', 'payment_status', 'rrr_number', 'payment_amount')
  list_display_links = ('institution', 'academic_session', 'payment_status', 'rrr_number')
  list_filter = ('institution', 'academic_session', 'payment_status', 'rrr_number')
  search_fields = ('institution', 'academic_session', 'payment_status', 'rrr_number')
  list_per_page = 25

admin.site.register(InstitutionPayment, InstitutionPaymentAdmin)


class AcademicSessionAdmin(admin.ModelAdmin):
    list_filter = ['updated', 'timestamp']
    list_display = ['name', 'slug', 'timestamp', 'updated']
    readonly_fields = ['updated', 'timestamp']
    search_fields = ['name', 'timestamp', 'slug', 'updated']
    
    class Meta:
        model = AcademicSession

    def short_title(self, obj):
        return obj.name[:3]

admin.site.register(AcademicSession, AcademicSessionAdmin)

