# Generated by Django 4.1.7 on 2023-03-02 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0009_subject_period_subject_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='period',
            field=models.TimeField(auto_now=True, choices=[(86400, 'день=86400'), (604800, 'неделя=604800'), (2419200, 'месяц=2419200')], max_length=10, null=True, verbose_name='Период'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='text',
            field=models.CharField(default='and here', max_length=100, verbose_name='Текст'),
        ),
    ]
