# Generated by Django 4.0.5 on 2024-04-22 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_alter_admissionquota_admission_quota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissionquota',
            name='admission_quota',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='admissionquota',
            unique_together={('institution', 'academic_session')},
        ),
    ]