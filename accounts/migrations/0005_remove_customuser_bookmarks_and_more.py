# Generated by Django 4.0 on 2022-04-07 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_email_alter_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bookmarks',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='completed',
        ),
    ]
