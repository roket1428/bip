# Generated by Django 5.0 on 2024-01-09 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bip_api', '0004_internlist_termslist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='karne',
            name='credits_sum',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='karne',
            name='gno',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='karne',
            name='points_sum',
            field=models.FloatField(),
        ),
    ]
