# Generated by Django 4.0.5 on 2023-06-17 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueIndexing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_no', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('academic_session', models.CharField(blank=True, choices=[('2022/2023', '2022/2023'), ('2023/2024', '2023/2024'), ('2024/2025', '2024/2025'), ('2025/2026', '2025/2026'), ('2026/2027', '2026/2027'), ('2027/2028', '2027/2028'), ('2028/2029', '2028/2029'), ('2029/2030', '2029/2030'), ('2030/2031', '2030/2031'), ('2031/2032', '2031/2032'), ('2032/2033', '2032/2033'), ('2033/2034', '2033/2034'), ('2034/2035', '2034/2035')], max_length=200, null=True)),
                ('index_number', models.CharField(max_length=200)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('indexing_payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.indexingpayment')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='issue_indexing', to='institutions.institutionprofile')),
                ('student_indexing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.studentindexing')),
                ('student_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.studentprofile')),
            ],
        ),
    ]
