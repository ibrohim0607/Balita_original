# Generated by Django 4.2.11 on 2024-04-16 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_post_tags_post_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tag',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='tags',
            new_name='category',
        ),
    ]
