# Generated by Django 3.2.9 on 2021-12-02 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_client_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name_plural': 'Clients'},
        ),
        migrations.AlterModelOptions(
            name='contract',
            options={'verbose_name_plural': 'Contracts'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name_plural': 'Events'},
        ),
    ]