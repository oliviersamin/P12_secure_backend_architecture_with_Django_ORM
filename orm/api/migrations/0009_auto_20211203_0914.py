# Generated by Django 3.2.9 on 2021-12-03 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20211202_1013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='support',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='support',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.support'),
        ),
    ]
