# Generated by Django 3.2.16 on 2024-06-29 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_profile_publication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='publication',
            new_name='post',
        ),
    ]
