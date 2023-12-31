# Generated by Django 4.2.2 on 2023-06-25 18:34

import ckeditor.fields
import core.helper
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('brand', models.CharField(blank=True, max_length=120)),
                ('selling_price', models.BigIntegerField()),
                ('offering_price', models.BigIntegerField()),
                ('image', models.ImageField(upload_to='product/', validators=[core.helper.file_size])),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('slug', models.SlugField(max_length=500, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('-updated_at',),
            },
        ),
    ]
