# Generated by Django 4.0.5 on 2024-05-01 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0004_alter_admissionquota_admission_quota_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institutionprofile',
            name='institution_type',
            field=models.CharField(choices=[('University', 'University'), ('College of Health', 'College of Health')], max_length=100),
        ),
    ]
