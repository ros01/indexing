from django.conf import settings
from django.db import models
from django.db.models import Prefetch, Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.text import slugify
from .choices import *
import datetime
from datetime import datetime
from datetime import date
from indexing_unit.utils import *



class InstitutionProfileQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    # def unused(self):
    #     return self.filter(Q(lecture__isnull=True)&Q(category__isnull=True))


class InstitutionProfileManager(models.Manager):
    def get_queryset(self):
        return InstitutionProfileQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()



class InstitutionProfile(models.Model):
    name           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True)
    course_type = models.CharField(max_length=100, blank=True)
    institution_type = models.CharField(max_length=100, choices = INSTITUTION_TYPE, blank=True)
    # description     = models.TextField()
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_no = models.CharField(max_length=100, blank=True) 
    accreditation_score = models.DecimalField(blank=True, max_digits=5, decimal_places=2)
    accreditation_date = models.DateTimeField(default=date.today)
    accreditation_type = models.CharField(max_length=100, choices = ACCREDITATION_TYPE, blank=True)
    address = models.TextField(blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = InstitutionProfileManager()

    def __str__(self): 
        return self.name

    @property
    def get_indexing_officer_profile_qs(self):
        indexingOfficerProfile = self.indexingofficerprofile_set.all()
        return indexingOfficerProfile 

    @property
    def get_issue_indexing_qs(self):
        issueIndexing = self.issueindexing_set.all()
        return issueIndexing 

    def get_student_profiles_list (self):
        return reverse("institutions:student_profiles_list")

    def get_create_student_profile_url (self):
        return reverse("institutions:create_student_profile", kwargs={"slug": self.slug})



    def get_absolute_url(self):
        #return "/videos/{slug_arg}/".format(slug_arg=self.slug)
        return reverse("indexing_unit:institution_detail", kwargs={"slug": self.slug})

def pre_save_institution_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.institution_type == 'University':
        instance.course_type = 'Medical Radiography'
    else:
         instance.course_type = 'Medical Image Processing Technician'

pre_save.connect(pre_save_institution_receiver, sender=InstitutionProfile)


class AcademicSession(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.title


class AdmissionQuota(models.Model):
    institution  = models.ForeignKey(InstitutionProfile, on_delete=models.SET_NULL, null=True)
    academic_session = models.CharField(max_length=100, choices = ACADEMIC_SESSION, blank=True)
    course_1 = models.CharField(max_length=100, choices = COURSE_TYPE, blank=True, null=True)
    admission_quota_1   = models.IntegerField(blank=True, null=True)
    course_2 = models.CharField(max_length=100, choices = COURSE_TYPE, blank=True, null=True)
    admission_quota_2   = models.IntegerField(blank=True, null=True)
    slug      = models.SlugField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    # objects = CategoryManager()

    def __str__(self):
        return self.academic_session

    # class Meta:
    #     unique_together = (('institution', 'academic_session'),)

    def get_absolute_url(self):
        return reverse("indexing_unit:admission_quota_detail", kwargs={"slug": self.slug})

def pre_save_admission_quota_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug2(instance)

pre_save.connect(pre_save_admission_quota_receiver, sender=AdmissionQuota)

    



class StudentProfileQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class StudentProfileManager(models.Manager):
    def get_queryset(self):
        return StudentProfileQuerySet(self.model, using=self._db)

    # def all(self):
    #     return self.get_queryset().all().prefetch_related('institution_set')

        # qs = InstitutionProfile.objects.all()
        # obj = qs.first()
        # institutionprofiles = obj.instituionprofile_set.all()


class StudentProfile(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    institution = models.ForeignKey(InstitutionProfile,  on_delete=models.DO_NOTHING)
    # indexing_payment = models.ForeignKey('IndexingPayment', null=True, blank=True, on_delete=models.DO_NOTHING)
    slug  = models.SlugField(blank=True)

    # reg_no = models.CharField(max_length=200)
    indexing_status = models.IntegerField(default=1)
    sex = models.CharField(max_length=200, choices = SEX, null=True, blank=True)
    dob = models.DateField(default=date.today, null=True, blank=True)
    marital_status = models.CharField(max_length=200, choices = MARRITAL_STATUS,  null=True, blank=True)
    nationality = models.CharField(max_length=200, choices = NATIONALITY,  null=True, blank=True)
    state_of_origin = models.CharField(max_length=200, choices = STATES,  null=True, blank=True)
    lga = models.CharField(max_length=200, null=True, blank=True)
    contact_address = models.CharField(max_length=200, null=True, blank=True)
    profile_creation_date = models.DateTimeField(default=datetime.now, blank=True)

    objects = StudentProfileManager()
    
    def __str__(self):
        return  str(self.student.get_full_name)

        

    @property
    def get_indexing_officer_profile_qs(self):
        indexingOfficerProfile = self.indexingofficerprofile_set.all()
        return indexingOfficerProfile

    
    def get_student_profile_details_url(self):
        return reverse('students:my_student_profile_details', kwargs={"slug": self.slug})

    def get_absolute_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }

        return reverse('institutions:student_profile_details', kwargs=url_kwargs)
        

def pre_save_student_profile_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug3(instance)

pre_save.connect(pre_save_student_profile_receiver, sender=StudentProfile)



class AdmissionTypeManager(models.Manager):
    def get_queryset(self):
        return AdmissionTypeQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()


class AdmissionType(models.Model):
    title           =  models.CharField(max_length=200, choices = ADMISSION_TYPE,  null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = AdmissionTypeManager()

    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        #return "/videos/{slug_arg}/".format(slug_arg=self.slug)
        return reverse("admission_type:detail", kwargs={"slug": self.slug})

def pre_save_admission_type_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_admission_type_receiver, sender=AdmissionType)


class UtmeGrade(models.Model):
    # title = models.CharField(max_length=120)
    # student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    examination_body = models.CharField(max_length=200, choices = EXAMINATION_BODY,  null=True, blank=True) 
    course_1 = models.CharField(max_length=200, choices = UTME_COURSES,  null=True, blank=True)
    course_1_grade = models.CharField(max_length=200, choices = UTME_COURSE_GRADES,  null=True, blank=True)
    course_2 = models.CharField(max_length=200, choices = UTME_COURSES,  null=True, blank=True)
    course_2_grade = models.CharField(max_length=200, choices = UTME_COURSE_GRADES,  null=True, blank=True)
    course_3 = models.CharField(max_length=200, choices = UTME_COURSES,  null=True, blank=True)
    course_3_grade = models.CharField(max_length=200, choices = UTME_COURSE_GRADES,  null=True, blank=True)
    course_4 = models.CharField(max_length=200, choices = UTME_COURSES,  null=True, blank=True)
    course_4_grade = models.CharField(max_length=200, choices = UTME_COURSE_GRADES,  null=True, blank=True)
    course_5 = models.CharField(max_length=200, choices = UTME_COURSES,  null=True, blank=True)
    course_5_grade = models.CharField(max_length=200, choices = UTME_COURSE_GRADES,  null=True, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.examination_body

class DeGrade(models.Model):
    # title = models.CharField(max_length=120)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    # admission_type = models.ForeignKey(AdmissionType, null=True, blank=True, on_delete=models.DO_NOTHING) 
    course_1 = models.CharField(max_length=200, choices = DE_COURSES,  null=True, blank=True)
    course_1_grade = models.CharField(max_length=200, choices = DE_COURSE_GRADES,  null=True, blank=True)
    course_2 = models.CharField(max_length=200, choices = DE_COURSES,  null=True, blank=True)
    course_2_grade = models.CharField(max_length=200, choices = DE_COURSE_GRADES,  null=True, blank=True)
    course_3 = models.CharField(max_length=200, choices = DE_COURSES,  null=True, blank=True)
    course_3_grade = models.CharField(max_length=200, choices = DE_COURSE_GRADES,  null=True, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student)

class TransferGrade(models.Model):
    # title = models.CharField(max_length=120)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    # admission_type = models.ForeignKey(AdmissionType, null=True, blank=True, on_delete=models.DO_NOTHING) 
    course_1 = models.CharField(max_length=200, choices = DE_COURSES,  null=True, blank=True)
    course_1_grade = models.CharField(max_length=200, choices = DE_COURSE_GRADES,  null=True, blank=True)
    course_2 = models.CharField(max_length=200, choices = DE_COURSES,  null=True, blank=True)
    course_2_grade = models.CharField(max_length=200, choices = DE_COURSE_GRADES,  null=True, blank=True)
    course_3 = models.CharField(max_length=200, choices = DE_COURSES,  null=True, blank=True)
    course_3_grade = models.CharField(max_length=200, choices = DE_COURSE_GRADES,  null=True, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student)



class StudentIndexing(models.Model):    
    student_profile = models.ForeignKey(StudentProfile,  null=True, blank=True, on_delete=models.DO_NOTHING)
    institution = models.ForeignKey(InstitutionProfile,  on_delete=models.DO_NOTHING)
    slug  = models.SlugField(blank=True)
    reg_no = models.CharField(max_length=200, unique=True)
    academic_session = models.CharField(max_length=200, choices = ACADEMIC_SESSION,  null=True, blank=True)
    admission_type = models.CharField(max_length=200, choices = ADMISSION_TYPE,  null=True, blank=True)
    utme_grade = models.ForeignKey(UtmeGrade, null=True, blank=True, on_delete=models.CASCADE) 
    de_grade = models.ForeignKey(DeGrade, null=True, blank=True, on_delete=models.DO_NOTHING)
    transfer_grade = models.ForeignKey(TransferGrade, null=True, blank=True, on_delete=models.DO_NOTHING) 
    indexing_status = models.IntegerField(default=2)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  str(self.student_profile)

    class Meta:
        unique_together = ('student_profile', 'reg_no')

    def get_absolute_url(self):
        return reverse('students:my_indexing_application_details', kwargs={"slug": self.slug})

    def get_indexing_url(self):
        return reverse('indexing_unit:student_indexing_application_details', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super(StudentIndexing, self).save(*args, **kwargs)
        self.indexing_status = 2
        self.student_profile.indexing_status = 3
        self.student_profile.save()

    # def save(self, *args, **kwargs):
    #     super(StudentIndexing, self).save(*args, **kwargs)
    #     self.indexing_status = 2
        
        
def pre_save_student_indexing_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug4(instance)

pre_save.connect(pre_save_student_indexing_receiver, sender=StudentIndexing)


class IndexingPayment(models.Model):
    institution = models.ForeignKey(InstitutionProfile, on_delete=models.DO_NOTHING)
    student_profile = models.ForeignKey(StudentProfile,  null=True, blank=True, on_delete=models.DO_NOTHING)
    student_indexing = models.ForeignKey(StudentIndexing,  null=True, blank=True, on_delete=models.DO_NOTHING)
    # institution_payment = models.ForeignKey("InstitutionPayment", null=True, blank=True, on_delete=models.DO_NOTHING)
    slug  = models.SlugField(blank=True)
    reg_no = models.CharField(max_length=200, unique=True)
    academic_session = models.CharField(max_length=200, choices = ACADEMIC_SESSION,  null=True, blank=True)
    payment_status = models.IntegerField(default=1)
    rrr_number = models.CharField(max_length=100)
    receipt_number = models.CharField(max_length=100)
    payment_amount = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, choices = PAYMENT_METHOD)
    payment_receipt = models.FileField(upload_to='%Y/%m/%d/')
    payment_date = models.DateField(default=date.today)  
    
    # class Meta:
    #     unique_together = ('institution','academic_session')
        
    def __str__(self):
        return  str(self.student_profile)

    def get_absolute_url(self):
        return reverse('students:my_indexing_application_details', kwargs={"slug": self.slug})

    def get_redirect_url(self):
        return reverse('institutions:student_indexing_payment_details', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super(IndexingPayment, self).save(*args, **kwargs)
        self.student_indexing.indexing_status = 3
        self.student_indexing.save()

def pre_save_student_indexing_payment_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug4(instance)

pre_save.connect(pre_save_student_indexing_payment_receiver, sender=IndexingPayment)



class InstitutionPayment(models.Model):
    institution = models.ForeignKey(InstitutionProfile, on_delete=models.DO_NOTHING)
    # student_profile = models.ForeignKey(StudentProfile,  null=True, blank=True, on_delete=models.DO_NOTHING)
    # student_indexing = models.ForeignKey(StudentIndexing,  null=True, blank=True, on_delete=models.DO_NOTHING)
    students_payments = models.ManyToManyField(IndexingPayment)
    slug  = models.SlugField(blank=True)
    academic_session = models.CharField(max_length=200, choices = ACADEMIC_SESSION,  null=True, blank=True)
    payment_status = models.IntegerField(default=1)
    rrr_number = models.CharField(max_length=100)
    receipt_number = models.CharField(max_length=100)
    payment_amount = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, choices = PAYMENT_METHOD)
    payment_receipt = models.FileField(upload_to='%Y/%m/%d/')
    payment_date = models.DateField(default=date.today)  
    
        
    def __str__(self):
        return  str(self.institution)

    def get_absolute_url(self):
        return reverse('institutions:institutions_indexing_payment_details', kwargs={"slug": self.slug})

    def get_indexing_url(self):
        return reverse('indexing_unit:institutions_indexing_payment_details', kwargs={"slug": self.slug})

def pre_save_institution_indexing_payment_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug7(instance)

pre_save.connect(pre_save_institution_indexing_payment_receiver, sender=InstitutionPayment)





class StudentAdmissionRecords(models.Model):    
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    faculty = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    registration_no = models.CharField(max_length=200)
    admission_type = models.ForeignKey(AdmissionType, null=True, blank=True, on_delete=models.DO_NOTHING)  
    academic_session = models.ForeignKey(AcademicSession, null=True, blank=True, on_delete=models.DO_NOTHING) 
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return  self.student


