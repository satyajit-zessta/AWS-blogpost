# Generated by Django 5.0 on 2024-01-11 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0008_alter_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='f_name', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='l_name', max_length=100),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
