# Generated by Django 3.2.13 on 2022-06-16 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edtech_app', '0004_alter_profile_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='logo',
        ),
    ]