# Generated by Django 5.0.7 on 2024-08-09 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0003_organization_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='content',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
