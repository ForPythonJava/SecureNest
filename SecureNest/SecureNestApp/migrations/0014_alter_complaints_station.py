# Generated by Django 4.2.2 on 2023-06-17 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SecureNestApp', '0013_alter_complaints_station'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaints',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SecureNestApp.policestation'),
        ),
    ]