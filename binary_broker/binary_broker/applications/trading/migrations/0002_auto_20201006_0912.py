# Generated by Django 3.1.1 on 2020-10-06 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='venture',
            field=models.DecimalField(choices=[(1, '1'), (2, '2'), (5, '5'), (10, '10'), (20, '20'), (50, '50'), (100, '100')], decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='mean_price',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalcommodity',
            name='mean_price',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalcommodity',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=10),
        ),
    ]
