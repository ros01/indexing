from django.contrib import admin

# Register your models here.
from .models import *
from institutions.models import StudentProfile


class StudentProfileInline(admin.TabularInline):
    model = StudentProfile
    prepopulated_fields = {"slug": ("student",)}
    extra = 1


class InstitutionProfileAdmin(admin.ModelAdmin):
    inlines = [StudentProfileInline]
    list_filter = ['updated', 'timestamp']
    list_display = ['id', 'name', 'slug', 'accreditation_score', 'accreditation_date', 'accreditation_type','updated', 'timestamp']
    readonly_fields = ['updated', 'timestamp', 'accreditation_score']
    search_fields = ['name', 'slug', 'accreditation_date', 'accreditation_type']
    
    class Meta:
        model = InstitutionProfile

    def short_title(self, obj):
        return obj.name[:3]

admin.site.register(InstitutionProfile, InstitutionProfileAdmin)


class AdmissionQuotaAdmin(admin.ModelAdmin):
    list_filter = ['updated', 'timestamp']
    list_display = ['id', 'institution', 'academic_session', 'slug', 'admission_quota']
    readonly_fields = ['updated', 'timestamp']
    search_fields = ['institution', 'academic_session', 'slug', 'admission_quota']
    
    class Meta:
        model = AdmissionQuota

    def short_title(self, obj):
        return obj.name[:3]

admin.site.register(AdmissionQuota, AdmissionQuotaAdmin)



class IssueIndexingAdmin(admin.ModelAdmin):
  list_display = ('student_profile', 'academic_session', 'matric_no', 'student_indexing', 'index_number', 'timestamp')
  list_display_links = ('student_profile', 'academic_session', 'student_indexing', 'index_number')
  list_filter = ('student_profile', 'academic_session', 'student_indexing', 'index_number')
  search_fields = ('student_profile', 'academic_session', 'student_indexing', 'index_number')
  list_per_page = 25


admin.site.register(IssueIndexing, IssueIndexingAdmin)