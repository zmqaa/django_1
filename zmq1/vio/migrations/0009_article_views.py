# Generated by Django 5.1.4 on 2024-12-17 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vio', '0008_delete_weatherdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
