# Generated by Django 4.1 on 2022-09-15 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('satta_king', '0017_everyhour_alter_dailybazar_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='everyhour',
            name='Number',
            field=models.CharField(max_length=5),
        ),
    ]
