# Generated by Django 4.0.5 on 2023-07-16 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0005_alter_degreeresults_degree_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionprofile',
            name='accreditation_due_date',
            field=models.DateField(null=True),
        ),
    ]
