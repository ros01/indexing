# Generated by Django 4.0.5 on 2023-06-20 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_alter_institutionprofile_accreditation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentindexing',
            name='utme_grade_result',
            field=models.FileField(blank=True, null=True, upload_to='%Y/%m/%d/'),
        ),
    ]