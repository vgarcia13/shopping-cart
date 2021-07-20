# Generated by Django 3.2.5 on 2021-07-20 02:01
import json

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def load_products_data(apps, schema_editor):
    Product = apps.get_model('api', 'Product')

    with open('products.json', encoding='utf-8') as data_file:
        json_data = json.loads(data_file.read())

        for product_data in json_data:
            product = Product.objects.create(
                title=product_data.get("title").replace("\x00", "\uFFFD"),
                type=product_data.get("type").replace("\x00", "\uFFFD"),
                description=product_data.get("description").replace("\x00", "\uFFFD"),
                filename=product_data.get("filename").replace("\x00", "\uFFFD"),
                height=product_data.get("height"),
                width=product_data.get("width"),
                price=product_data.get("price"),
                rating=product_data.get("rating")
            )
            product.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('filename', models.CharField(max_length=128)),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('price', models.FloatField()),
                ('rating', models.IntegerField()),
            ],
            options={
                'verbose_name': 'product',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Generic Cart', max_length=100)),
                ('total', models.FloatField(blank=True, null=True)),
                ('products', models.ManyToManyField(related_name='products', to='api.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'cart',
            },
        ),
        migrations.RunPython(load_products_data)
    ]