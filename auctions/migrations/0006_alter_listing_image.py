# Generated by Django 4.0.4 on 2022-05-05 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, default='images/default.jpeg', null=True, upload_to='images/'),
        ),
    ]
