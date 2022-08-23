# Generated by Django 4.0.1 on 2022-07-16 08:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('attendanceID', models.AutoField(primary_key=True, serialize=False)),
                ('studentId', models.IntegerField(default=0)),
                ('percentage', models.IntegerField(default=0)),
                ('date', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'attendance',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('modified_at', models.DateField(default=datetime.date.today, verbose_name='Date')),
            ],
            options={
                'db_table': 'document',
            },
        ),
        migrations.CreateModel(
            name='RegisteredStudents',
            fields=[
                ('RegID', models.AutoField(primary_key=True, serialize=False)),
                ('courseId', models.IntegerField(default=0)),
                ('studentId', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'RegisteredStudents',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentId', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=40)),
                ('uname', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('imageEncodings', models.TextField(max_length=50000)),
                ('profile_pic', models.ImageField(default='ahsan.jpg', upload_to='')),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('submissionID', models.AutoField(primary_key=True, serialize=False)),
                ('assignmentId', models.IntegerField(default=0)),
                ('studentId', models.IntegerField(default=0)),
                ('file', models.FileField(upload_to='')),
            ],
            options={
                'db_table': 'submission',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacherId', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=40)),
                ('fname', models.CharField(max_length=40)),
                ('uname', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'teacher',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('couseId', models.AutoField(primary_key=True, serialize=False)),
                ('courseCode', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('credits', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=1000)),
                ('teacher', models.ForeignKey(db_column='teacherId', on_delete=django.db.models.deletion.DO_NOTHING, to='virtualapp.teacher')),
            ],
            options={
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignmentID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=5000)),
                ('file', models.FileField(upload_to='')),
                ('dueDate', models.CharField(max_length=50)),
                ('assignDate', models.CharField(max_length=50)),
                ('assignmentNo', models.IntegerField(default=0)),
                ('couseId', models.ForeignKey(db_column='couseId', on_delete=django.db.models.deletion.DO_NOTHING, to='virtualapp.course')),
            ],
            options={
                'db_table': 'assignment',
            },
        ),
    ]
