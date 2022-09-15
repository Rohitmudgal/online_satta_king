# Generated by Django 4.1 on 2022-09-14 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('satta_king', '0014_two_pm_triplepana_two_pm_singlepana_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyBazar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Milan Morning', 'Milan Morning'), ('Welcome Morning', 'Welcome Morning'), ('Kalyan Morning', 'Kalyan Morning'), ('Madhur Morning', 'Madhur Morning'), ('Sridevi', 'Sridevi'), ('Time Bazar', 'Time Bazar'), ('Madhur Day', 'Madhur Day'), ('New Kalyan', 'New Kalyan'), ('Milan Day', 'Milan Day'), ('Rajdhani Day', 'Rajdhani Day'), ('Supreme Day', 'Supreme Day'), ('Kalyan', 'Kalyan'), ('Sridevi Night', 'Sridevi Night'), ('Madhur Night', 'Madhur Night'), ('New Main Mumbai', 'New Main Mumbai'), ('Milan Night', 'Milan Night'), ('Kalyan Night', 'Kalyan Night'), ('Rajdhani Night', 'Rajdhani Night'), ('Main Bazar', 'Main Bazar')], max_length=100)),
                ('Number', models.CharField(max_length=8)),
            ],
        ),
    ]
