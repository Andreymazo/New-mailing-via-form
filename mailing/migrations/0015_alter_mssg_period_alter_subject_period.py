# Generated by Django 4.1.7 on 2023-03-13 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0014_alter_mssg_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mssg',
            name='period',
            field=models.IntegerField(blank=True, choices=[(120, 'день=120'), (604800, 'неделя=604800'), (2419200, 'месяц=2419200')], null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='period',
            field=models.IntegerField(choices=[(86400, '3min=120'), (604800, 'неделя=604800'), (2419200, 'месяц=2419200')], default=86400, verbose_name='Период'),
        ),
    ]
