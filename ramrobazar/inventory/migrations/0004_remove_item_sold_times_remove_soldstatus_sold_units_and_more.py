# Generated by Django 4.0 on 2022-10-21 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0003_alter_media_alt_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='sold_times',
        ),
        migrations.RemoveField(
            model_name='soldstatus',
            name='sold_units',
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.user'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='inventory.item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, default='No Description Provided', help_text='format: required', verbose_name='item description'),
        ),
        migrations.AlterField(
            model_name='item',
            name='reported_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='reported_item', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='users_wishlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_wishlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='media',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='media', to='inventory.item'),
        ),
        migrations.AlterField(
            model_name='soldstatus',
            name='date_sold',
            field=models.DateField(blank=True, help_text='date when item was sold', null=True, verbose_name='date sold'),
        ),
        migrations.CreateModel(
            name='ItemDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='format: required', max_length=50, verbose_name='detail title')),
                ('value', models.CharField(help_text='format: required', max_length=150, verbose_name='detail value')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_detail', to='inventory.item')),
            ],
            options={
                'verbose_name': 'Item Detail',
                'verbose_name_plural': 'Item Details',
            },
        ),
    ]
