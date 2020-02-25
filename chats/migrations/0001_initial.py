# Generated by Django 2.2.1 on 2019-06-22 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_type', models.CharField(max_length=10)),
                ('missed', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=True)),
                ('started_at', models.TimeField(auto_now_add=True, null=True)),
                ('ended_at', models.TimeField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('size', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('confirm', models.BooleanField(default=True)),
                ('first', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_thread_first', to='accounts.PlayMateUser')),
                ('second', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_thread_second', to='accounts.PlayMateUser')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=10000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='chat-imgaes')),
                ('files', models.FileField(blank=True, null=True, upload_to='chat-files')),
                ('status', models.CharField(default='sent', max_length=10)),
                ('seen', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('thread', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chats.Thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.PlayMateUser', verbose_name='sender')),
            ],
        ),
        migrations.CreateModel(
            name='ChatList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.IntegerField(default=0)),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chats.ChatMessage')),
                ('thread', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chats.Thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.PlayMateUser')),
            ],
        ),
        migrations.CreateModel(
            name='CallList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(blank=True, max_length=10, null=True)),
                ('details', models.CharField(blank=True, max_length=10, null=True)),
                ('counter', models.IntegerField(default=0)),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.Call')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.PlayMateUser')),
            ],
        ),
        migrations.AddField(
            model_name='call',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.Thread'),
        ),
        migrations.AddField(
            model_name='call',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.PlayMateUser'),
        ),
    ]