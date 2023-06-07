# Generated by Django 4.2.1 on 2023-06-06 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget_planner_app', '0002_post_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=500)),
                ('expenditure', models.BooleanField(default=False)),
                ('recurring', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=22)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_planner_app.item')),
            ],
        ),
        migrations.CreateModel(
            name='Actual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=22)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_planner_app.item')),
            ],
        ),
    ]