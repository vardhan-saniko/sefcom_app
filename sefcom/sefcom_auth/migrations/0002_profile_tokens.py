# Generated by Django 4.1.4 on 2022-12-25 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sefcom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tokens',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
