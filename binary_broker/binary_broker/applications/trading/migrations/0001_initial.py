# Generated by Django 3.1.1 on 2020-10-01 12:19

import binary_broker.applications.trading.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mean_price', models.FloatField(default=10.0)),
                ('price', models.FloatField(default=10.0)),
            ],
            options={
                'verbose_name_plural': 'commodities',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCommodity',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mean_price', models.FloatField(default=10.0)),
                ('price', models.FloatField(default=10.0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical commodity',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.BooleanField(choices=[(True, 'up'), (False, 'down')], null=True)),
                ('venture', models.FloatField(choices=[(1, '1'), (2, '2'), (5, '5'), (10, '10'), (20, '20'), (50, '50'), (100, '100')])),
                ('duration', binary_broker.applications.trading.models.TimedeltaField(choices=[(10, '10'), (30, '30'), (60, '60'), (120, '120')])),
                ('time_start', models.TimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
