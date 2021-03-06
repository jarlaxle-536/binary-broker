# Generated by Django 3.1.1 on 2020-10-16 17:06

import binary_broker.applications.trading.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, validators=[binary_broker.applications.trading.validators.validate_not_empty])),
                ('mean_price', models.DecimalField(decimal_places=2, default=10, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, default=10, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('Demo', 'Demo'), ('Real', 'Real')], default='Demo', max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalAsset',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, validators=[binary_broker.applications.trading.validators.validate_not_empty])),
                ('mean_price', models.DecimalField(decimal_places=2, default=10, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, default=10, max_digits=10)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical asset',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('Demo', 'Demo'), ('Real', 'Real')], max_length=20, validators=[binary_broker.applications.trading.validators.validate_not_empty])),
                ('direction_up', models.BooleanField(choices=[(True, 'up'), (False, 'down')])),
                ('venture', models.DecimalField(choices=[(0, '0 $'), (1, '1 $'), (2, '2 $'), (5, '5 $'), (10, '10 $'), (20, '20 $'), (50, '50 $'), (100, '100 $'), (1000000, '1000000 $')], decimal_places=2, max_digits=10)),
                ('duration', models.IntegerField(choices=[(1, '1 second'), (10, '10 seconds'), (30, '30 seconds'), (60, '1 minute'), (120, '2 minutes')])),
                ('price_when_created', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('time_start', models.DateTimeField(auto_now_add=True)),
                ('result', models.IntegerField(blank=True, choices=[(1, 'Won'), (0, 'Equal'), (-1, 'Lost')], null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.asset')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
    ]
