# Generated by Django 5.1.4 on 2025-01-11 21:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id_kategori', models.AutoField(primary_key=True, serialize=False)),
                ('nama_kategori', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id_status', models.AutoField(primary_key=True, serialize=False)),
                ('nama_status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Produk',
            fields=[
                ('id_produk', models.AutoField(primary_key=True, serialize=False)),
                ('nama_produk', models.CharField(max_length=100)),
                ('harga', models.DecimalField(decimal_places=2, max_digits=10)),
                ('kategori', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produks', to='myapp.kategori')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produks', to='myapp.status')),
            ],
        ),
    ]
