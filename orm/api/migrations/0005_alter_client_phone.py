# Generated by Django 3.2.9 on 2021-11-30 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_client_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.IntegerField(blank=True, max_length=20),
        ),
    ]
