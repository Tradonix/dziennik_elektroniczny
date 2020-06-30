# Generated by Django 3.0.7 on 2020-06-30 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20200625_1244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subjects',
            old_name='teachers',
            new_name='teacher',
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('title', models.CharField(max_length=32)),
                ('is_read', models.BooleanField(default=False)),
                ('send_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_send', to=settings.AUTH_USER_MODEL)),
                ('send_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
