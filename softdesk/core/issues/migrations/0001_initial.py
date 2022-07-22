# Generated by Django 4.0.6 on 2022-07-21 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_alter_project_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('desc', models.CharField(blank=True, max_length=512)),
                ('tag', models.CharField(choices=[('B', 'Bug'), ('T', 'Task'), ('I', 'Improvement')], max_length=1)),
                ('priority', models.CharField(choices=[('C', 'Critical'), ('M', 'Major'), ('N', 'Normal'), ('MN', 'Minor')], max_length=2)),
                ('status', models.CharField(choices=[('TD', 'To Do'), ('P', 'In Progress'), ('D', 'Done')], default='TD', max_length=2)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assignee_user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignee', to=settings.AUTH_USER_MODEL)),
                ('author_user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]