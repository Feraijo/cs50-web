# Generated by Django 2.0.3 on 2020-05-12 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0007_auto_20200512_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pending', models.BooleanField(default=True)),
                ('adds', models.ManyToManyField(blank=True, to='orders.Addition')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.MenuItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='adds',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]