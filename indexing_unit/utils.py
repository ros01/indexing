import random
import string

from .models import *
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.text import slugify
import uuid
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template import loader
from rrbnindexing.settings import EMAIL_HOST_PASSWORD
from django.http import HttpResponse
import sendgrid
from django.views.decorators.csrf import csrf_exempt
from sendgrid.helpers.mail import Mail,Email,Content
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import get_template, render_to_string
from django.template import Context
AUTH_USER_MODEL='accounts.User'

def unique_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def generate_slug(instance, field_path, new_slug=None):
    """
    Generic slug generator.
    - instance: model instance
    - field_path: field or nested fields separated by '.' (dot notation)
    - new_slug: optional manually provided slug
    """
    if new_slug:
        slug = new_slug
    else:
        # Resolve the field_path, e.g., "student.last_name"
        value = instance
        for attr in field_path.split('.'):
            value = getattr(value, attr)
        slug = slugify(value)

    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    
    if qs.exists():
        from indexing_unit.utils import unique_string_generator  # import inside to avoid circular import
        string_unique = unique_string_generator()
        newly_created_slug = f"{slug}-{string_unique}"
        return generate_slug(instance, field_path, new_slug=newly_created_slug)

    return slug


def create_slug0(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.last_name)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug

def create_slug0_stub(data):
    base = f"{data['first_name']}-{data['last_name']}"
    slug = slugify(base)
    return f"{slug}-{uuid.uuid4().hex[:6]}"


def create_slug(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.name)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug




def create_slug2(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.academic_session)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug


# utils.py
def create_slug3_from_user(user):
    slug = slugify(user.last_name)
    Klass = StudentProfile
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        slug = f"{slug}-{string_unique}"
    return slug



def create_slug3(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.student.last_name)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug

def create_slug4(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.student_profile.student.last_name)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug


def create_slug5(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.indexing_officer.last_name)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug


def create_slug6(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.student.last_name)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug



def create_slug7(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.institution.name)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug



# def reset_password(user, request):
#     c = {
#         'email': user.email,
#         'domain': request.META['HTTP_HOST'],
#         'site_name': 'indexing',
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'user': user,
#         'token': default_token_generator.make_token(user),
#         'protocol': 'https' if request.is_secure() else 'http',
#     }
#     subject_template_name = 'accounts/password_reset_subject.txt'
#     email_template_name = 'accounts/password_reset_email.html'
#     subject = loader.render_to_string(subject_template_name, c)
#     # Email subject *must not* contain newlines
#     subject = ''.join(subject.splitlines())
#     email = loader.render_to_string(email_template_name, c)
#     try:
#         to_email = Email(user.email)
#         from_email = Email("institute@rrbn.gov.ng")
#         content = Content('text/html', email)
#         message = Mail(from_email, subject, to_email, content)
#         message.content_subtype = 'html'
#         sg = sendgrid.SendGridAPIClient(apikey=EMAIL_HOST_PASSWORD)
#         sg.client.mail.send.post(request_body=message.get())
#     except Exception as e:
#         print(e)


def reset_password(user, request):
    context = {}
    context['email'] = user.email 
    context['domain'] = request.META['HTTP_HOST'] 
    context['site_name'] = 'indexing' 
    context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
    context['user'] = user 
    context['token'] = default_token_generator.make_token(user)
    context["protocol"] = 'https' if request.is_secure() else 'http'
    subject = 'Password Change Request'
    html_template = 'accounts/password_reset_email1.html'
    html_message = render_to_string(html_template, context)
    try:        
        from_email ="institute@rrbn.gov.ng"
        to_email = [user.email]
        message = EmailMessage(subject, html_message, from_email, to_email)
        message.content_subtype = 'html'
        message.send()
    except Exception as e:
        print(e)


def reset_user_password(user, request):
    context = {}
    context['email'] = user.email 
    context['domain'] = request.META['HTTP_HOST'] 
    context['site_name'] = 'indexing' 
    context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
    context['user'] = user 
    context['token'] = default_token_generator.make_token(user)
    context["protocol"] = 'https' if request.is_secure() else 'http'
    subject = 'Password Change Request'
    html_template = 'accounts/password_reset_email3.html'
    html_message = render_to_string(html_template, context)
    try:        
        from_email ="institute@rrbn.gov.ng"
        to_email = [user.email]
        message = EmailMessage(subject, html_message, from_email, to_email)
        message.content_subtype = 'html'
        message.send()
    except Exception as e:
        print(e)







