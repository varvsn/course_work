# Generated by Django 2.0 on 2017-12-20 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0008_auto_20171220_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopsettings',
            name='footer',
        ),
        migrations.RemoveField(
            model_name='shopsettings',
            name='shop_name',
        ),
        migrations.AddField(
            model_name='shopsettings',
            name='value',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
