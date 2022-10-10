# Generated by Django 4.0.5 on 2022-10-06 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='server-key')),
                ('nickname', models.CharField(max_length=20, null=True, unique=True)),
                ('phone', models.CharField(max_length=11, null=True)),
                ('client_secret', models.CharField(max_length=12, unique=True, verbose_name='client-key')),
                ('created_dt', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_dt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'seller',
            },
        ),
    ]