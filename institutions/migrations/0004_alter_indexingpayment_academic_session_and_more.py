# Generated by Django 4.0.5 on 2023-07-12 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_alter_degreeresults_degree_result_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexingpayment',
            name='academic_session',
            field=models.CharField(choices=[('2022/2023', '2022/2023'), ('2023/2024', '2023/2024'), ('2024/2025', '2024/2025'), ('2025/2026', '2025/2026'), ('2026/2027', '2026/2027'), ('2027/2028', '2027/2028'), ('2028/2029', '2028/2029'), ('2029/2030', '2029/2030'), ('2030/2031', '2030/2031'), ('2031/2032', '2031/2032'), ('2032/2033', '2032/2033'), ('2033/2034', '2033/2034'), ('2034/2035', '2034/2035')], default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='indexingpayment',
            name='receipt_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
