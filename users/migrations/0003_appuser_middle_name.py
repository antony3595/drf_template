# Generated by Django 3.2.22 on 2023-10-18 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_appuser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='middle_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество'),
        ),
    ]
