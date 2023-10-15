from django.conf import settings
from django.db import models
from django.db.models import Prefetch, Q
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from .choices import *
import datetime
from datetime import datetime
from datetime import date
from indexing_unit.utils import *
from multiselectfield import MultiSelectField


class AcademicSession(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.name

    def get_absolute_url(self):
        return reverse("indexing_unit:academic_session_detail", kwargs={"slug": self.slug})

def pre_save_academic_session_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_academic_session_receiver, sender=AcademicSession)


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
    accreditation_date = models.DateField(null=True)
    accreditation_type = models.CharField(max_length=100, choices = ACCREDITATION_TYPE, blank=True)
    accreditation_due_date = models.DateField(null=True)
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

    def get_reg_absolute_url(self):
        #return "/videos/{slug_arg}/".format(slug_arg=self.slug)
        return reverse("registration:institution_detail", kwargs={"slug": self.slug})

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



class AdmissionQuota(models.Model):
    institution  = models.ForeignKey(InstitutionProfile, on_delete=models.SET_NULL, null=True)
    # academic_session = models.CharField(max_length=100, choices = ACADEMIC_SESSION, blank=True)
    academic_session = models.ForeignKey(AcademicSession,  on_delete=models.CASCADE)
    admission_quota  = models.IntegerField(blank=True, null=True)
    slug      = models.SlugField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return self.academic_session

    
    def get_admission_quota_url(self):
        return reverse("institutions:admission_quota_detail", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return reverse("indexing_unit:admission_quota_detail", kwargs={"slug": self.slug})

    def get_reg_absolute_url(self):
        return reverse("registration:admission_quota_detail", kwargs={"slug": self.slug})

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
    # admission_type = models.CharField(max_length=100, choices = EXAMINATION_BODY, blank=True)
    slug  = models.SlugField(blank=True)
    # academic_session = models.CharField(max_length=200, null=True, blank=True)
    academic_session = models.ForeignKey(AcademicSession,  on_delete=models.CASCADE)
    indexing_status = models.IntegerField(default=1)
    sex = models.CharField(max_length=200, choices = SEX, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=200, choices = MARRITAL_STATUS,  null=True, blank=True)
    nationality = models.CharField(max_length=200, choices = NATIONALITY,  null=True, blank=True)
    state_of_origin = models.CharField(max_length=200, choices = STATES,  null=True, blank=True)
    lga = models.CharField(max_length=200, null=True, blank=True)
    contact_address = models.CharField(max_length=200, null=True, blank=True)
    profile_creation_date = models.DateTimeField(default=datetime.now, blank=True)

    objects = StudentProfileManager()
    
    def __str__(self):
        return  str(self.student.get_full_name)


    def get_utmeresult (self):
        utmeresult = self.utmeresult_set.first()
        return utmeresult  

    @property
    def get_indexing_officer_profile_qs(self):
        indexingOfficerProfile = self.indexingofficerprofile_set.all()
        return indexingOfficerProfile

    
    def get_student_profile_details_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('students:my_student_profile_details',kwargs=url_kwargs)

    
    def update_student_profile_details_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('students:update_profile',kwargs=url_kwargs)

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
    # matric_no = models.CharField(max_length=200, unique=True)
    # student_profile = models.ForeignKey(StudentProfile,  null=True, blank=True, on_delete=models.CASCADE)
    examination_body = models.CharField(max_length=200, choices = EXAMINATION_BODY,  null=True)
    physics_score = models.CharField(max_length=200, choices = UTME_SCORES,  null=True)
    chemistry_score = models.CharField(max_length=200, choices = UTME_SCORES,  null=True)
    biology_score = models.CharField(max_length=200, choices = UTME_SCORES,  null=True)
    english_score = models.CharField(max_length=200, choices = UTME_SCORES,  null=True)
    mathematics_score = models.CharField(max_length=200, choices = UTME_SCORES,  null=True)
    utme_grade_result = models.FileField(upload_to='%Y/%m/%d/')
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('matric_no','student_profile')

    def __str__(self):
        return self.examination_body


class GceAlevels(models.Model):
    # matric_no = models.CharField(max_length=200, unique=True)
    # student_profile = models.ForeignKey(StudentProfile,  null=True, blank=True, on_delete=models.CASCADE)
    examination_body = models.CharField(max_length=200, choices = GCE_EXAM_BODY,  null=True) 
    chemistry_score = models.CharField(max_length=200, choices = GCE_A_LEVELS_SCORES,  null=True)
    biology_score = models.CharField(max_length=200, choices = GCE_A_LEVELS_SCORES,  null=True)
    physics_score = models.CharField(max_length=200, choices = GCE_A_LEVELS_SCORES,  null=True)
    gce_alevels_result = models.FileField(upload_to='%Y/%m/%d/')
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('matric_no','student_profile')

    def __str__(self):
        return str(self.examination_body)


class DegreeResults(models.Model):
    # matric_no = models.CharField(max_length=200, unique=True)
    # student_profile = models.ForeignKey(StudentProfile,  null=True, blank=True, on_delete=models.CASCADE)
    degree_type = models.CharField(max_length=200, choices = DEGREE_TYPE,  null=True) 
    institution = models.CharField(max_length=200, choices = INSTITUTIONS,  null=True)
    course = models.CharField(max_length=200, choices = DEGREE_COURSES,  null=True)
    course_grade = models.CharField(max_length=200, choices = DEGREE_COURSE_GRADES,  null=True)
    degree_result = models.FileField(upload_to='%Y/%m/%d/')
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('matric_no','student_profile')

    def __str__(self):
        return str(self.degree_type)


class TransferGrade(models.Model):
    # matric_no = models.CharField(max_length=200, unique=True)
    # student_profile = models.ForeignKey(StudentProfile,  null=True, blank=True, on_delete=models.DO_NOTHING)
    course = models.CharField(max_length=200, choices = TRANSFER_COURSES,  null=True)
    institution = models.CharField(max_length=200, choices = INSTITUTIONS,  null=True)
    degree_type = models.CharField(max_length=200, choices = DEGREE_TYPE,  null=True) 
    year_of_study = models.CharField(max_length=200, choices = YEAR_OF_STUDY,  null=True) 
    course_grade = models.CharField(max_length=200, choices = DEGREE_COURSE_GRADES,  null=True)
    academic_transcript = models.FileField(upload_to='%Y/%m/%d/')
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.degree_type)


class StudentIndexing(models.Model):    
    student_profile = models.ForeignKey(StudentProfile,  null=True, blank=True, on_delete=models.CASCADE)
    institution = models.ForeignKey(InstitutionProfile,  on_delete=models.DO_NOTHING)
    slug  = models.SlugField(blank=True)
    matric_no = models.CharField(max_length=200, unique=True)
    # academic_session = models.CharField(max_length=200, choices = ACADEMIC_SESSION)
    academic_session = models.ForeignKey(AcademicSession,  on_delete=models.CASCADE)
    admission_type = models.CharField(max_length=200, null=True, blank=True)
    utme_grade = models.ForeignKey(UtmeGrade, on_delete=models.CASCADE, null=True) 
    gce_alevels = models.ForeignKey(GceAlevels, on_delete=models.CASCADE, null=True)
    degree_result = models.ForeignKey(DegreeResults, on_delete=models.CASCADE, null=True)
    transfer_grade = models.ForeignKey(TransferGrade, on_delete=models.CASCADE, null=True) 
    # utme_grade_result = models.FileField(null=True, blank=True, upload_to='%Y/%m/%d/')
    indexing_status = models.IntegerField(default=1)
    verification_status = models.IntegerField(default=1)
    board_verification_status = models.IntegerField(default=1)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  str(self.slug)

    class Meta:
        unique_together = ('student_profile', 'matric_no')


    def get_absolute_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('students:my_indexing_application_details', kwargs=url_kwargs)


    def get_application_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('institutions:student_indexing_details', kwargs=url_kwargs)

    def get_student_application_details_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('students:my_indexing_application_details', kwargs=url_kwargs)


    def get_application_details_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('institutions:student_indexing_application_details', kwargs=url_kwargs)


    def get_verification_details_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('institutions:student_indexing_verification_details', kwargs=url_kwargs)

    # def get_institution_indexing_url(self):
    #     return reverse('institutions:student_indexing_application_details', kwargs={"slug": self.slug})

    # def get_application_url(self):
    #     return reverse('institutions:student_indexing_details', kwargs={"slug": self.slug})

    def get_index_url(self):
        return reverse('indexing_unit:student_indexing_application_details', kwargs={"slug": self.slug})

    def get_indexing_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('indexing_unit:student_indexing_details', kwargs=url_kwargs)



    def get_reg_indexing_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('registration:student_indexing_details', kwargs=url_kwargs)


    def get_reg_indexed_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('registration:students_post_indexing_details', kwargs=url_kwargs)


    def get_indexing_number_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('indexing_unit:students_indexing_details', kwargs=url_kwargs)



    def get_reg_indexing_number_url(self):
        url_kwargs={
            'islug': self.institution.slug,
            'sslug': self.slug,
        }
        return reverse('registration:students_indexing_details', kwargs=url_kwargs)


    def save(self, *args, **kwargs):
        super(StudentIndexing, self).save(*args, **kwargs)
        # self.indexing_status = 2
        self.student_profile.indexing_status = 3
        self.student_profile.save()

    # def save(self, *args, **kwargs):
    #     super(StudentIndexing, self).save(*args, **kwargs)
    #     self.indexing_status = 2
        
        
def pre_save_student_indexing_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug4(instance)

    if instance.gce_alevels:
        instance.admission_type = 'DE'
    elif instance.degree_result:
        instance.admission_type = 'DE'
    elif instance.transfer_grade:
        instance.admission_type = 'DE'
    else:
        instance.admission_type = 'UTME'

pre_save.connect(pre_save_student_indexing_receiver, sender=StudentIndexing)






class IndexingPayment(models.Model):
    institution = models.ForeignKey(InstitutionProfile, on_delete=models.DO_NOTHING)
    student_profile = models.ForeignKey(StudentProfile,  null=True, blank=True, on_delete=models.CASCADE)
    student_indexing = models.ForeignKey(StudentIndexing,  null=True, blank=True, on_delete=models.CASCADE)
    # institution_payment = models.ForeignKey("InstitutionPayment", null=True, blank=True, on_delete=models.DO_NOTHING)
    slug  = models.SlugField(blank=True)
    matric_no = models.CharField(max_length=200, unique=True)
    # academic_session = models.CharField(max_length=200, choices = ACADEMIC_SESSION)
    academic_session = models.ForeignKey(AcademicSession,  on_delete=models.CASCADE)
    payment_status = models.IntegerField(default=1)
    indexing_status = models.IntegerField(default=1)
    payment_verification_status = models.IntegerField(default=1)
    rrr_number = models.CharField(max_length=100, null=True, blank=True)
    receipt_number = models.CharField(max_length=100, null=True, blank=True)
    payment_amount = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, choices = PAYMENT_METHOD)
    payment_receipt = models.FileField(null=True, blank=True, upload_to='%Y/%m/%d/')
    payment_date = models.DateField(default=date.today)  
    
    # class Meta:
    #     unique_together = ('institution','academic_session')
        
    def __str__(self):
        return  str(self.student_profile)

    @property
    def get_indexing_students_list(self):
        studentsList = self.institutionpayment_set.all()
        return studentsList 

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
    # academic_session = models.CharField(max_length=200, choices = ACADEMIC_SESSION,  null=True, blank=True)
    academic_session = models.ForeignKey(AcademicSession,  on_delete=models.CASCADE)
    payment_status = models.IntegerField(default=1)
    rrr_number = models.CharField(max_length=100)
    # receipt_number = models.CharField(max_length=100)
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


    def get_reg_indexing_url(self):
        return reverse('registration:institutions_indexing_payment_details', kwargs={"slug": self.slug})

    # def save(self, *args, **kwargs):       
    #     for student in self.students_payments.all():
    #         student.student_indexing.indexing_status  = 4
    #         student.save()
    #     super(InstitutionPayment, self).save(*args, **kwargs)

def pre_save_institution_indexing_payment_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug7(instance)

pre_save.connect(pre_save_institution_indexing_payment_receiver, sender=InstitutionPayment)

def post_save_institution_payment_receiver(sender, instance,  *args, **kwargs):
    for student in instance.students_payments.all():
        student.payment_verification_status  = 2
        student.save()

m2m_changed.connect(post_save_institution_payment_receiver, sender=InstitutionPayment.students_payments.through)


# @receiver(post_save, sender=InstitutionPayment)
# def my_handler(sender, instance, **kwargs):
#     for student in instance.students_payments.all():
#         student.student_indexing.indexing_status = 4
#         student.save()





class StudentAdmissionRecords(models.Model):    
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    faculty = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    registration_no = models.CharField(max_length=200)
    admission_type = models.ForeignKey(AdmissionType, null=True, blank=True, on_delete=models.DO_NOTHING)
    academic_session = models.ForeignKey(AcademicSession,  on_delete=models.CASCADE)  
    # academic_session = models.ForeignKey(AcademicSession, null=True, blank=True, on_delete=models.DO_NOTHING) 
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return  self.student


