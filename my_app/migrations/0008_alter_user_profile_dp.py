# Generated by Django 5.0 on 2024-02-15 11:52

import my_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0007_alter_user_profile_dp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='dp',
            field=models.ImageField(blank=True, null=True, upload_to=my_app.models.filepath),
        ),
    ]
