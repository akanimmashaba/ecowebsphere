# Generated by Django 3.2.8 on 2021-10-20 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user_type',
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('STUDENT', 'STUDENT'), ('LANDLORD', 'LANDLORD')], default='STUDENT', max_length=8),
        ),
    ]