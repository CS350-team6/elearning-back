# Generated by Django 4.2.1 on 2023-05-30 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0004_userinfo_validation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='jwttoken',
            name='blacklist',
            field=models.BooleanField(default=False),
        ),
    ]
