# Generated by Django 2.2.1 on 2019-06-22 13:08

import accounts.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiry', models.DateTimeField(blank=True, null=True)),
                ('validated', models.BooleanField(default=False)),
                ('used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PlayMateUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', models.CharField(max_length=15, unique=True, verbose_name='Phone number')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('otp', models.CharField(blank=True, max_length=6, verbose_name='otp')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', accounts.models.PlayMateUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(blank=True, max_length=50, null=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('chatDistance', models.IntegerField(default=10)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('chat_gender', models.CharField(blank=True, max_length=6, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('age', models.CharField(blank=True, max_length=4, null=True)),
                ('height', models.CharField(blank=True, max_length=4, null=True)),
                ('body_type', models.CharField(blank=True, max_length=15, null=True)),
                ('dating', models.BooleanField(default=False)),
                ('hookup', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, upload_to='profile_image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='accounts.PlayMateUser')),
            ],
        ),
        migrations.CreateModel(
            name='PmAuthToken',
            fields=[
                ('digest', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('token_key', models.CharField(db_index=True, max_length=8)),
                ('salt', models.CharField(max_length=16, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expiry', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token_set', to='accounts.PlayMateUser')),
            ],
        ),
    ]
