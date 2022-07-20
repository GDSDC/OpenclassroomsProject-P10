# Generated by Django 4.0.6 on 2022-07-20 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_contributor'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='permission',
            field=models.CharField(choices=[('R', 'ReadOnly'), ('RW', 'ReadAndWrite')], default='RW', max_length=2),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='role',
            field=models.CharField(choices=[('A', 'Author'), ('C', 'Contributor')], default='C', max_length=1),
        ),
    ]