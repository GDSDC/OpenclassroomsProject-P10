# Generated by Django 4.0.6 on 2022-08-22 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('desc', models.CharField(blank=True, max_length=512)),
                ('tag', models.CharField(choices=[('BUG', 'Bug'), ('TASK', 'Task'), ('IMPROVEMENT', 'Improvement')], max_length=12)),
                ('priority', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], max_length=6)),
                ('status', models.CharField(choices=[('TODO', 'To Do'), ('INPROGRESS', 'In Progress'), ('DONE', 'Done')], default='TODO', max_length=12)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
