# Generated by Django 4.1.7 on 2023-03-01 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0008_subject_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='period',
            field=models.TimeField(auto_now=True, choices=[(86400, 'день=86400'), (604800, 'неделя=604800'), (2419200, 'месяц=2419200')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]