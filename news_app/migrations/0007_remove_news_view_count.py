# Generated by Django 4.2.2 on 2023-07-14 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0006_news_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
    ]
