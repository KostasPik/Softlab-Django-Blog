# Generated by Django 4.0 on 2022-01-14 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_post_options_alter_post_tags'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['active'], name='posts_comme_active_77e66b_idx'),
        ),
    ]