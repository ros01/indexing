from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.utils.text import slugify
# from .choices import *
from datetime import datetime
from datetime import date
from .utils import *
from institutions.models import *
# Create your models here.
# from courses.utils import create_slug



class IssueIndexing(models.Model):    
    student_profile = models.ForeignKey(StudentProfile,  null=True, blank=True, on_delete=models.CASCADE)
    matric_no = models.CharField(max_length=200, unique=True)
    institution = models.ForeignKey(InstitutionProfile, related_name = "issue_indexing", on_delete=models.DO_NOTHING)
    slug  = models.SlugField(blank=True)
    # academic_session = models.CharField(max_length=200, choices = ACADEMIC_SESSION,  null=True, blank=True)
    academic_session = models.ForeignKey(AcademicSession,  on_delete=models.CASCADE)
    student_indexing = models.ForeignKey(StudentIndexing, null=True, on_delete=models.CASCADE)
    # indexing_payment = models.ForeignKey(IndexingPayment, null=True, on_delete=models.CASCADE)
    index_number = models.CharField(max_length=200, unique=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('matric_no','index_number')

    def __str__(self):
        return  str(self.student_profile)

    

    def get_absolute_url(self):
        return reverse('registration:student_indexing_number_details', kwargs={"slug": self.slug}) 

    def get_indexing_absolute_url(self):
        return reverse('indexing_unit:student_indexing_number_details', kwargs={"slug": self.slug})

    def get_institution_absolute_url(self):
        return reverse('institutions:student_indexing_number_details', kwargs={"slug": self.slug})

    def get_student_absolute_url(self):
        return reverse('students:my_indexing_number_details', kwargs={"slug": self.slug})



    def save(self, *args, **kwargs):
        super(IssueIndexing, self).save(*args, **kwargs)
        self.student_indexing.verification_status = "indexed"
        self.student_indexing.indexing_status = "indexed"
        # self.indexing_payment.payment_status = 4
        self.student_indexing.save()  
        # self.indexing_payment.save()   

def pre_save_issue_indexing_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        from indexing_unit.utils import generate_slug
        instance.slug = generate_slug(instance, "student_profile.student.last_name")

pre_save.connect(pre_save_issue_indexing_receiver, sender=IssueIndexing)  





