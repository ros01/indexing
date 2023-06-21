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


class DeGradeAdmin(admin.ModelAdmin):
  list_display = ('student', 'timestamp')
  list_display_links = ('student', 'timestamp')
  list_filter = ('student', 'timestamp')
  search_fields = ('student', 'timestamp')
  list_per_page = 25


admin.site.register(DeGrade, DeGradeAdmin)


class TransferGradeAdmin(admin.ModelAdmin):
  list_display = ('student', 'timestamp')
  list_display_links = ('student', 'timestamp')
  list_filter = ('student', 'timestamp')
  search_fields = ('student', 'timestamp')
  list_per_page = 25


admin.site.register(TransferGrade, TransferGradeAdmin)



class StudentIndexingAdmin(admin.ModelAdmin):
  list_display = ('student_profile', 'slug', 'academic_session', 'admission_type', 'indexing_status', 'verification_status', 'timestamp', 'updated')
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
  list_display = ('institution', 'academic_session', 'payment_status', 'rrr_number', 'receipt_number', 'payment_amount')
  list_display_links = ('institution', 'academic_session', 'payment_status', 'rrr_number', 'receipt_number')
  list_filter = ('institution', 'academic_session', 'payment_status', 'rrr_number', 'receipt_number')
  search_fields = ('institution', 'academic_session', 'payment_status', 'rrr_number', 'receipt_number')
  list_per_page = 25


  # def list_students(self, obj):
  #       return "\n".join([a.students for a in obj.student_profile.all()])


admin.site.register(InstitutionPayment, InstitutionPaymentAdmin)




