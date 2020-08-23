# Generated by Django 3.0.7 on 2020-08-23 02:56

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
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_name', models.CharField(max_length=100)),
                ('org_name', models.CharField(blank=True, max_length=100)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('hours', models.TimeField()),
                ('notes', models.TextField(blank=True, max_length=250)),
                ('street', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('state', models.CharField(blank=True, max_length=100)),
                ('location', models.IntegerField(blank=True, max_length=100)),
                ('phone', models.IntegerField(blank=True, max_length=10)),
                ('url', models.CharField(blank=True, max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]