from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import date
import uuid
# from multiselectfield import MultiSelectField
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from .choices import *
from indexing_unit.utils import *
from indexing_unit.models import *
from django.db.models.signals import pre_save, post_save

# Create your models here.


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        return self._create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):

    ROLE = (
        ('Student', 'Student'),
        ('Indexing Officer', 'Indexing Officer'),
        ('Indexing Unit', 'Indexing Unit'),
        ('Registrar', 'Registrar'),
        ('Registration', 'Registration'),
        ('Sysadmin', 'Sysadmin'),
        )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    slug  = models.SlugField(blank=True, null=True, unique=True)
    phone_no = models.CharField(max_length=100, blank=True)
    matric_no = models.CharField(max_length=200, blank=True)
    role = models.CharField (max_length=20, choices = ROLE, blank=True, default='Student')
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

      
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    #def get_absolute_url(self):
        #return reverse("accounts:profile_detail", kwargs={"id": self.id})

    def __str__(self):
        return self.email


    @property
    def get_indexing_officer_profile(self):
        indexingOfficerProfile = self.indexingofficerprofile_set.first()
        return indexingOfficerProfile 

   
    @property 
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


    def get_short_name(self):
        return self.email


def post_save_user_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug0(instance)

pre_save.connect(post_save_user_receiver, sender=User)


class IndexingOfficerProfile(models.Model):
    indexing_officer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    institution = models.ForeignKey(InstitutionProfile, null=True, blank=True, on_delete=models.CASCADE)
    slug  = models.SlugField(blank=True, null=True, unique=True)
    status = models.BooleanField(default=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  str(self.indexing_officer)

    def get_absolute_url(self):
        return reverse("indexing_unit:indexing_officer_detail", kwargs={"slug": self.slug})


    def get_reg_absolute_url(self):
        return reverse("registration:indexing_officer_detail", kwargs={"slug": self.slug})

def post_save_indexing_officer_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug5(instance)

pre_save.connect(post_save_indexing_officer_receiver, sender=IndexingOfficerProfile)

    