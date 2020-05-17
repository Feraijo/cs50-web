# Generated by Django 2.0.3 on 2020-05-12 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200512_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='tops',
        ),
        migrations.AddField(
            model_name='addition',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='adds',
            field=models.ManyToManyField(blank=True, to='orders.Addition'),
        ),
    ]