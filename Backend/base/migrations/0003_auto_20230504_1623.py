# Generated by Django 3.2.19 on 2023-05-04 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20230504_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='preferred_end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='preferred_start',
            field=models.DateTimeField(null=True),
        ),
    ]
