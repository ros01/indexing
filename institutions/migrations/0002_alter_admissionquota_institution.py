# Generated by Django 4.0.5 on 2024-01-02 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissionquota',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.institutionprofile'),
        ),
    ]
