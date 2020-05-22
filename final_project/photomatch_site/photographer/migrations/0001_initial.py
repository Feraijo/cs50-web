# Generated by Django 3.0.6 on 2020-05-22 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Human',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='')),
                ('first_name', models.CharField(max_length=256)),
                ('second_name', models.CharField(max_length=256)),
                ('age', models.PositiveSmallIntegerField()),
                ('gender', models.CharField(choices=[('ns', 'Not specified'), ('m', 'Male'), ('f', 'Female'), ('nb', 'Non-binary')], default='ns', max_length=2)),
            ],
        ),
    ]
