from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
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
    reg_no = models.CharField(max_length=200, unique=True)
    institution = models.ForeignKey(InstitutionProfile, related_name = "issue_indexing", on_delete=models.DO_NOTHING)
    slug  = models.SlugField(blank=True)
    academic_session = models.CharField(max_length=200, choices = ACADEMIC_SESSION,  null=True, blank=True)
    student_indexing = models.ForeignKey(StudentIndexing, null=True, related_name='st_indexing', on_delete=models.CASCADE)
    index_number = models.CharField(max_length=200)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    
    

    def __str__(self):
        return  str(self.student_profile)

    

    def get_absolute_url(self):
        return reverse('indexing_unit:student_indexing_number_details', kwargs={"slug": self.slug}) 

    def save(self, *args, **kwargs):
        super(IssueIndexing, self).save(*args, **kwargs)
        self.student_indexing.indexing_status = 5
        self.student_indexing.save()   

def pre_save_issue_indexing_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug4(instance)

pre_save.connect(pre_save_issue_indexing_receiver, sender=IssueIndexing)   
