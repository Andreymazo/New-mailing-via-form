# Generated by Django 4.1.7 on 2023-03-02 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0010_alter_subject_period_alter_subject_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='period',
            field=models.IntegerField(choices=[(86400, 'день=86400'), (604800, 'неделя=604800'), (2419200, 'месяц=2419200')], default=86400, max_length=10, verbose_name='Период'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='topic',
            field=models.CharField(default='ande', max_length=100, verbose_name='Тема сообщения в форме сабджекта'),
        ),
    ]
