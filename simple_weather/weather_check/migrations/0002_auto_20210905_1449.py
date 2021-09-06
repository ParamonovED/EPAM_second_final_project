# Generated by Django 3.2.6 on 2021-09-05 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_check', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='date_day',
            field=models.IntegerField(verbose_name='weather day'),
        ),
        migrations.AlterField(
            model_name='city',
            name='date_month',
            field=models.IntegerField(verbose_name='weather month'),
        ),
        migrations.AlterField(
            model_name='city',
            name='date_year',
            field=models.IntegerField(verbose_name='weather year'),
        ),
    ]