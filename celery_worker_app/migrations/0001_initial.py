# Generated by Django 4.2.10 on 2025-03-18 06:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('DONE', 'Done'), ('FAILED', 'Failed')], db_index=True, default='PENDING', max_length=20)),
                ('task_name', models.CharField(db_index=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('input_data', models.JSONField(default=dict)),
                ('result', models.JSONField(blank=True, default=dict, null=True)),
                ('related_table', models.CharField(blank=True, max_length=100, null=True)),
                ('related_id', models.CharField(blank=True, max_length=255, null=True)),
                ('operation', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
