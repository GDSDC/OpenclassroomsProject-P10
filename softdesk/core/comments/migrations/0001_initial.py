# Generated by Django 4.0.6 on 2022-08-22 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=512)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
