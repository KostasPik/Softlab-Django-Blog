# Generated by Django 4.0 on 2022-04-08 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_remove_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='blog_tags', to='posts.Tag'),
        ),
    ]
