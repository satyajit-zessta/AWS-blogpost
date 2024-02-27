# Generated by Django 5.0 on 2024-01-10 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0006_alter_post_tags_alter_tagging_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='posts_tags', to='blogging.tagging'),
        ),
        migrations.AlterField(
            model_name='tagging',
            name='posts',
            field=models.ManyToManyField(related_name='tags_posts', to='blogging.post'),
        ),
    ]