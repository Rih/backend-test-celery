# Generated by Django 3.0.8 on 2021-07-03 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='scheduled',
            new_name='scheduled_at',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='option',
        ),
        migrations.AddField(
            model_name='menu',
            name='celery_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='menu',
            name='celery_task_id',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='suggestion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
