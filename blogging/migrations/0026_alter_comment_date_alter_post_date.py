# Generated by Django 5.0 on 2024-02-22 10:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0025_post_image_alter_comment_date_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(default=datetime.date(2024, 2, 22)),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(default=datetime.date(2024, 2, 22)),
        ),
    ]