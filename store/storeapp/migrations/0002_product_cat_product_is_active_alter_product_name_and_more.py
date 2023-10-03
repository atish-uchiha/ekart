# Generated by Django 4.2.4 on 2023-08-23 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cat',
            field=models.CharField(choices=[('1', 'Mobile'), ('2', 'Shoes'), ('3', 'Cloths')], default=0, max_length=10, verbose_name='Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='qty',
            field=models.IntegerField(verbose_name='Quantity'),
        ),
    ]
