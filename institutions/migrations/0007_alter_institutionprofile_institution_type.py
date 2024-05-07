# Generated by Django 4.0.5 on 2024-05-01 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0006_alter_institutionprofile_institution_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institutionprofile',
            name='institution_type',
            field=models.CharField(choices=[('University', 'University'), ('College of Health', 'College of Health')], default='Select Institution', max_length=100),
        ),
    ]