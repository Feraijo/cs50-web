# Generated by Django 2.0.3 on 2020-05-12 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0002_auto_20200508_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adds', models.ManyToManyField(to='orders.SubAddition')),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_large', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('price_small', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('name', models.CharField(max_length=128)),
                ('number_of_toppings', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.ItemType')),
            ],
        ),
        migrations.AddField(
            model_name='cartitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.MenuItem'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='tops',
            field=models.ManyToManyField(to='orders.Topping'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together={('name', 'item_type')},
        ),
    ]
