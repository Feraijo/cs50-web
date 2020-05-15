# Generated by Django 2.0.3 on 2020-05-14 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20200513_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='amount',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='adds',
            field=models.ManyToManyField(blank=True, related_name='purchases', to='orders.Addition'),
        ),
    ]
