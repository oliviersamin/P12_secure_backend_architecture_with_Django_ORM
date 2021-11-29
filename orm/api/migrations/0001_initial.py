# Generated by Django 3.2.9 on 2021-11-20 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=25)),
                ('last_name', models.CharField(blank=True, max_length=25)),
                ('email', models.CharField(blank=True, max_length=100, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('mobile', models.CharField(blank=True, max_length=20)),
                ('company_name', models.CharField(blank=True, max_length=250)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('is_confirmed_client', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contract_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('signed', models.BooleanField(default=False)),
                ('amount', models.FloatField(blank=True)),
                ('payment_due', models.DateTimeField(blank=True)),
                ('client', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.client')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('event_performed', models.BooleanField(default=False)),
                ('attendees', models.IntegerField(blank=True)),
                ('event_date', models.DateTimeField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('contract', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.contract')),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('mobile', models.CharField(blank=True, max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.event')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('mobile', models.CharField(blank=True, max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='sales',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.sales'),
        ),
    ]
