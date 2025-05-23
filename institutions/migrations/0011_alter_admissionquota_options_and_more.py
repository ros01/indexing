# Generated by Django 4.0.5 on 2025-04-22 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0010_alter_degreeresults_institution_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admissionquota',
            options={'ordering': ['-academic_session']},
        ),
        migrations.AlterField(
            model_name='utmegrade',
            name='examination_body',
            field=models.CharField(choices=[('WAEC', 'WAEC'), ('NECO', 'NECO'), ('NABTEB', 'NABTEB'), ('WAEC & NECO', 'WAEC & NECO'), ('WAEC & NABTEB', 'WAEC & NABTEB'), ('NECO & NABTEB', 'NECO & NABTEB')], max_length=200, null=True),
        ),
    ]
