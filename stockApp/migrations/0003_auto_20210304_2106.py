# Generated by Django 3.1.7 on 2021-03-04 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockApp', '0002_remove_stock_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash',
            name='user_cash',
            field=models.FloatField(default=10000.0),
        ),
    ]