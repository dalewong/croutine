# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-31 11:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField()),
            ],
            options={
                'db_table': 'Cart',
            },
        ),
        migrations.CreateModel(
            name='Goods_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=20)),
                ('goods_description', tinymce.models.HTMLField()),
                ('goods_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('goods_stock', models.IntegerField()),
                ('goods_msg', tinymce.models.HTMLField()),
                ('goods_unit', models.CharField(max_length=20)),
                ('goods_pic_url', models.ImageField(upload_to='uploads/')),
            ],
            options={
                'db_table': 'Goods_info',
            },
        ),
        migrations.CreateModel(
            name='Goods_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_list_name', models.CharField(max_length=20)),
                ('goods_list_class', models.CharField(max_length=20)),
                ('goods_list_pic', models.ImageField(upload_to='uploads/')),
            ],
            options={
                'db_table': 'Goods_list',
            },
        ),
        migrations.CreateModel(
            name='Ord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.IntegerField(default=0)),
                ('submit_date', models.DateTimeField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('isPay', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'Ord',
            },
        ),
        migrations.CreateModel(
            name='Order_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('odetail_goods_num', models.IntegerField(default=0)),
                ('odetail_totalprice', models.IntegerField(default=0)),
                ('detail_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.Ord')),
                ('odetail_goods_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.Goods_info')),
            ],
            options={
                'db_table': 'Order_detail',
            },
        ),
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_address', tinymce.models.HTMLField()),
                ('receiver_name', models.CharField(max_length=20)),
                ('receiver_phone', models.CharField(max_length=20)),
                ('receiver_email', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Receiver',
            },
        ),
        migrations.CreateModel(
            name='User_db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('user_password', models.CharField(max_length=20)),
                ('user_phone', models.CharField(max_length=20)),
                ('user_email', models.CharField(max_length=20)),
                ('user_address', tinymce.models.HTMLField()),
            ],
            options={
                'db_table': 'User_db',
            },
        ),
        migrations.AddField(
            model_name='receiver',
            name='receiver_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.User_db'),
        ),
        migrations.AddField(
            model_name='ord',
            name='order_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.User_db'),
        ),
        migrations.AddField(
            model_name='goods_info',
            name='goods_list_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.Goods_list'),
        ),
        migrations.AddField(
            model_name='cart',
            name='goods_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.Goods_info'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.User_db'),
        ),
    ]