# Generated by Django 5.0 on 2024-01-18 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0014_rename_comment_post_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ManyToManyField(blank=True, null=True, related_name='comments_post', to='blogging.post'),
        ),
    ]