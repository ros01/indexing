# Generated by Django 4.0.5 on 2023-07-12 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexing_unit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issueindexing',
            name='index_number',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='issueindexing',
            unique_together={('matric_no', 'index_number')},
        ),
    ]