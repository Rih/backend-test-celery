# Generated by Django 3.0.8 on 2021-07-03 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20210703_0345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskmenu',
            old_name='menu_id',
            new_name='menu',
        ),
    ]
