# Generated by Django 5.1.3 on 2024-12-14 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hirehub', '0018_rename_skill_userprofile_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='skills',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]
