# Generated by Django 3.0.7 on 2021-10-22 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('age', models.TextField()),
                ('gender', models.TextField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]
