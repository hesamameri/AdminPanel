# Generated by Django 4.2.1 on 2023-06-18 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('chart_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'chart',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ChartCity',
            fields=[
                ('chart_city_id', models.AutoField(primary_key=True, serialize=False)),
                ('chart_id', models.IntegerField(blank=True, null=True)),
                ('city_type', models.CharField(blank=True, max_length=6, null=True)),
                ('city_id', models.IntegerField()),
            ],
            options={
                'db_table': 'chart_city',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ChartRole',
            fields=[
                ('chart_role_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'chart_role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Obj',
            fields=[
                ('obj_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'obj',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ObjDocument',
            fields=[
                ('obj_document_id', models.AutoField(primary_key=True, serialize=False)),
                ('source_type', models.CharField(max_length=255)),
                ('source_id', models.IntegerField()),
                ('document_type', models.CharField(max_length=255)),
                ('uri', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('hash', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'obj_document',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ObjItem',
            fields=[
                ('obj_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'obj_item',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ObjItemCity',
            fields=[
                ('obj_item_city_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'obj_item_city',
                'db_table_comment': 'هدف از طراحی جدول فوق برای انبارها بوده است\nکه هر انبار به شهرهایی سرویس میدهد و انباردار مربوطه فقط فاکتروهای منطقه خودش را مشاهده کند\nهمپوشانی انبار و منطقه اگر وجود داشته باشد امکان ارسال دوباره کالا خواهد شد',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ObjItemConfirmer',
            fields=[
                ('obj_item_confirmer_id', models.AutoField(primary_key=True, serialize=False)),
                ('register_hierarchical', models.IntegerField(blank=True, db_comment='آیا زیر دست های چارت فوق میتوانند ثبت کننده باشند', null=True)),
                ('confirmer_hierarchical', models.IntegerField()),
                ('depo_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'obj_item_confirmer',
                'db_table_comment': 'انبارها\nثثبت کننده\nتایید کننده کیفیت\nشمارش کننده انبار\n\nلوازم مصرفی\nچه کسی صدور میزند اگر خالی بود همه میتوانند صدور بزنند\nچه کسی میتواند این کالا را تایید کند که خریداری شود و نمیتواند خالی باشد\nتصویب کننده اگر تصویب کننده کالا داشت باید تصویب شود وگرنه تایید کننده تصویب کننده هم خواهد بود',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ObjItemSpec',
            fields=[
                ('obj_item_spec_id', models.AutoField(primary_key=True, serialize=False)),
                ('val', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'obj_item_spec',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ObjSpec',
            fields=[
                ('obj_spec_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('data_type', models.CharField(blank=True, max_length=100, null=True)),
                ('default_value', models.TextField(blank=True, null=True)),
                ('requirement', models.IntegerField(blank=True, null=True)),
                ('order_id', models.IntegerField(blank=True, null=True)),
                ('min_len', models.IntegerField(blank=True, null=True)),
                ('max_len', models.IntegerField(blank=True, null=True)),
                ('min_value', models.FloatField(blank=True, null=True)),
                ('max_value', models.FloatField(blank=True, null=True)),
                ('pattern', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'obj_spec',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ObjType',
            fields=[
                ('obj_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('has_bom', models.IntegerField(blank=True, null=True)),
                ('child_length', models.IntegerField(blank=True, null=True)),
                ('order_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'obj_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('is_otp', models.IntegerField(blank=True, null=True)),
                ('otp', models.CharField(blank=True, max_length=255, null=True)),
                ('vendor_code', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('branch_name', models.CharField(blank=True, max_length=255, null=True)),
                ('branch_site', models.CharField(blank=True, max_length=255, null=True)),
                ('internal_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserChart',
            fields=[
                ('user_chart_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_chart',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('user_role_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'user_role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserVendor',
            fields=[
                ('user_vendor_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'user_vendor',
                'db_table_comment': 'ارتباط نام کاربری و کد مشتری ثبت شده در سییستم',
                'managed': False,
            },
        ),
    ]
