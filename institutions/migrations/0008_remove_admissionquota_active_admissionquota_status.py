# Generated by Django 4.0.5 on 2024-08-03 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0007_remove_academicsession_active_admissionquota_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admissionquota',
            name='active',
        ),
        migrations.AddField(
            model_name='admissionquota',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
