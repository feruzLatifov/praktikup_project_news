# Generated by Django 4.2.2 on 2023-07-04 15:41

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0003_rename_emai_contact_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
    ]
