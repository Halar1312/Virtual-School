# Generated by Django 3.2.5 on 2021-07-23 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='assignmentNo',
            field=models.IntegerField(default=0),
        ),
    ]