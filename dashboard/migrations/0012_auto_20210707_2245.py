# Generated by Django 3.0.8 on 2021-07-07 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0011_auto_20210706_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='menu',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='taskmenu',
            name='menu',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='taskmenu', to='dashboard.Menu'),
        ),
    ]
