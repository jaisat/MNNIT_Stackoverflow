# Generated by Django 2.1.7 on 2021-02-26 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_comment_downvote_upvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.TextField(default=''),
        ),
    ]
