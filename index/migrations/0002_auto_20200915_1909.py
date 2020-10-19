# Generated by Django 2.0.6 on 2020-09-15 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbook',
            name='book_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tbook',
            name='new_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tcar',
            name='count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tcar',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='index.TUser'),
        ),
    ]
