# Generated by Django 4.0.4 on 2022-04-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_humis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.IntegerField()),
                ('time', models.DateTimeField()),
            ],
        ),
    ]
