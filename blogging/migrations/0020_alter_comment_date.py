# Generated by Django 5.0 on 2024-01-30 12:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0019_alter_comment_email_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 30)),
        ),
    ]
