# Generated by Django 4.0.4 on 2022-05-28 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, unique, max-100', max_length=100, unique=True, verbose_name='brand name')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, max_length=100', max_length=100, verbose_name='category name')),
                ('slug', models.SlugField(help_text='format: required, letters, numbers, underscore or hyphen', max_length=150, verbose_name='category url')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, help_text='format: not required', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='inventory.category', verbose_name='parent category')),
            ],
            options={
                'verbose_name': 'product category',
                'verbose_name_plural': 'product categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('web_id', models.CharField(help_text='format: required, unique', max_length=50, unique=True, verbose_name='product web id')),
                ('slug', models.SlugField(help_text='format: required, letters, numbers, underscore or hyphen', max_length=255, verbose_name='product url')),
                ('name', models.CharField(help_text='format: required, max_length=250', max_length=250, verbose_name='product name')),
                ('description', models.TextField(help_text='format: required', verbose_name='product description')),
                ('price', models.DecimalField(decimal_places=2, help_text='format: max price = 99999.99', max_digits=7, verbose_name='Cost of Product')),
                ('available_units', models.IntegerField(default=0, verbose_name='available units')),
                ('sold_units', models.IntegerField(default=0, verbose_name='sold units')),
                ('is_visible', models.BooleanField(default=True, help_text='format: true->product is visiible', verbose_name='product visibility')),
                ('is_blocked', models.BooleanField(default=False, help_text='format: true->product is blocked', verbose_name='product blocked')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='format: Y-m-d H:M:S', verbose_name='date product created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='format: Y-m-d H:M:S', verbose_name='date product last updated')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='brand_products', to='inventory.brand')),
                ('category', mptt.fields.TreeManyToManyField(to='inventory.category')),
                ('reported_by', models.ManyToManyField(blank=True, related_name='reported_product', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to=settings.AUTH_USER_MODEL)),
                ('users_wishlist', models.ManyToManyField(blank=True, related_name='user_wishlist_product', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('web_id', models.CharField(help_text='format: required, unique', max_length=50, unique=True, verbose_name='service web id')),
                ('slug', models.SlugField(help_text='format: required, letters, numbers, underscore or hyphen', max_length=255, verbose_name='service url')),
                ('name', models.CharField(help_text='format: required, max_length=250', max_length=250, verbose_name='service name')),
                ('description', models.TextField(help_text='format: required', verbose_name='service description')),
                ('price_min', models.DecimalField(decimal_places=2, help_text='format: max price = 99999.99', max_digits=7, verbose_name='Minimum Cost of Service')),
                ('price_max', models.DecimalField(decimal_places=2, help_text='format: max price = 99999.99', max_digits=7, verbose_name='Maximum Cost of Service')),
                ('no_sold_times', models.IntegerField(default=0, verbose_name='No. of times service is sold')),
                ('available_date_start', models.DateField(blank=True, help_text='date when service starts. can be null.', null=True, verbose_name='service start date')),
                ('available_date_end', models.DateField(blank=True, help_text='date when service ends. can be null.', null=True, verbose_name='service end date')),
                ('available_time_start', models.TimeField(blank=True, help_text='time when service starts. can be null.', null=True, verbose_name='service start time')),
                ('available_time_end', models.TimeField(blank=True, help_text='time when service ends. can be null.', null=True, verbose_name='service end time')),
                ('location', models.TextField(blank=True, null=True, verbose_name='available locations')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='format: Y-m-d H:M:S', verbose_name='date service created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='format: Y-m-d H:M:S', verbose_name='date service last updated')),
                ('category', mptt.fields.TreeManyToManyField(to='inventory.category')),
                ('reported_by', models.ManyToManyField(blank=True, related_name='reported_service', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='services', to=settings.AUTH_USER_MODEL)),
                ('users_wishlist', models.ManyToManyField(blank=True, related_name='user_wishlist_service', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceSoldStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_status', models.BooleanField(default=False, help_text='format: default=false, true=buyer confirms buying', verbose_name='bought by buyer')),
                ('seller_status', models.BooleanField(default=False, help_text='format: default=false, true=seller confirms selling', verbose_name='sold by seller')),
                ('no_sold_times', models.IntegerField(default=0, help_text='number of times buyer bought the service')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sold_status', to='inventory.service')),
            ],
            options={
                'verbose_name': 'service sold status',
                'verbose_name_plural': 'service sold status',
            },
        ),
        migrations.CreateModel(
            name='ProductSoldStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_status', models.BooleanField(default=False, help_text='format: default=false, true=buyer confirms buying', verbose_name='bought by buyer')),
                ('seller_status', models.BooleanField(default=False, help_text='format: default=false, true=seller confirms selling', verbose_name='sold by seller')),
                ('sold_units', models.IntegerField(default=0, help_text='number of units sold to buyer')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sold_status', to='inventory.product')),
            ],
            options={
                'verbose_name': 'product sold status',
                'verbose_name_plural': 'product sold status',
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default_product.jpg', help_text='format: required, default-default_product.png', upload_to='products', verbose_name='product image')),
                ('alt_text', models.CharField(help_text='format: required, max-255', max_length=255, verbose_name='alternative text')),
                ('is_feature', models.BooleanField(default=False, help_text='format: default=false, true=default/main image', verbose_name='default/main image')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_media', to='inventory.product')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='service_media', to='inventory.service')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_commented', models.DateTimeField(auto_now_add=True, verbose_name='date commented')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='inventory.comment')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='inventory.product')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='inventory.service')),
            ],
            options={
                'ordering': ['-date_commented'],
            },
        ),
    ]
