# Generated by Django 4.1.1 on 2022-09-13 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricingrule',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.property'),
        ),
    ]
