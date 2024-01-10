# Generated by Django 5.0 on 2024-01-03 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bip_api', '0003_terms'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('major', models.CharField(max_length=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('intern_time', models.IntegerField()),
                ('status', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='TermsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=15)),
                ('lecture_code', models.CharField(max_length=15)),
                ('lecture_name', models.CharField(max_length=75)),
                ('t', models.IntegerField()),
                ('u', models.IntegerField()),
                ('k', models.IntegerField()),
                ('akts', models.IntegerField()),
            ],
        ),
    ]
