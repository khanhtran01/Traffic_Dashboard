# Generated by Django 4.0.4 on 2022-04-24 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Humis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('humi', models.IntegerField()),
                ('time', models.DateTimeField()),
            ],
        ),
    ]