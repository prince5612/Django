# Generated by Django 5.0 on 2024-03-11 13:44

import django.db.models.deletion
import my_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0012_alter_user_count_follower_cnt_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_img', models.ImageField(blank=True, null=True, upload_to=my_app.models.filepath1)),
                ('like_cnt', models.IntegerField()),
                ('captions', models.CharField(max_length=200)),
                ('user_pro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.user_profile')),
                ('user_pro_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.user_profile_img')),
            ],
        ),
    ]
