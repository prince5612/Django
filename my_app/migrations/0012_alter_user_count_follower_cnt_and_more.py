# Generated by Django 5.0 on 2024-03-05 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0011_alter_post_post_img_followers_following_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_count',
            name='follower_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user_count',
            name='following_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user_count',
            name='post_cnt',
            field=models.IntegerField(default=0),
        ),
    ]