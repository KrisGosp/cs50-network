# Generated by Django 5.0.6 on 2024-07-12 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='timestamp',
            new_name='created_at',
        ),
    ]