# Generated by Django 4.2.2 on 2023-06-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SecureNestApp', '0016_programs'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaints',
            name='utype',
            field=models.CharField(default='CHILD', max_length=100),
        ),
    ]
