# Generated by Django 4.2.11 on 2025-04-24 08:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.TextField(default='')),
                ('status', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=255)),
                ('start_time', models.CharField(max_length=255)),
                ('current_stage', models.IntegerField()),
                ('stage_end_time', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.application')),
            ],
        ),
        migrations.CreateModel(
            name='AuctionBid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.IntegerField()),
                ('value', models.JSONField(null=True)),
                ('timestamp', models.CharField(max_length=255)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.auction')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.application')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField()),
                ('content', models.TextField(default='', max_length=255)),
                ('likes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('logo', models.TextField(default='')),
                ('description', models.TextField(default='', max_length=100)),
                ('website', models.TextField(default='')),
                ('industry', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=20)),
                ('founded_year', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.TextField(default='', max_length=100)),
                ('solution', models.TextField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField(default='')),
                ('requirements', models.TextField(null=True)),
                ('salary_min', models.FloatField()),
                ('salary_max', models.FloatField()),
                ('city', models.CharField(max_length=20)),
                ('metro', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=30)),
                ('schedule', models.CharField(max_length=30)),
                ('experiense', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('type_of_money', models.CharField(default='', max_length=3)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.company')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='')),
                ('message_type', models.CharField(max_length=255)),
                ('metadata', models.JSONField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.chat')),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=10, null=True)),
                ('profession', models.CharField(max_length=50)),
                ('experience', models.TextField()),
                ('education', models.CharField(max_length=50)),
                ('institutionName', models.CharField(max_length=50)),
                ('graduationYear', models.CharField(max_length=4)),
                ('specialization', models.CharField(max_length=50)),
                ('skills', models.CharField(max_length=255)),
                ('contacts', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=15)),
                ('last_name', models.CharField(blank=True, max_length=15)),
                ('avatar', models.TextField(blank=True, default='')),
                ('date_of_birth', models.CharField(blank=True, max_length=10)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=20)),
                ('region', models.CharField(blank=True, max_length=20)),
                ('district', models.CharField(blank=True, max_length=20)),
                ('publish_phone', models.BooleanField(default=False)),
                ('publish_status', models.BooleanField(default=False)),
                ('role', models.CharField(default='student', max_length=10)),
                ('password', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_signup', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='farmeritem',
            name='farmer',
        ),
        migrations.RemoveField(
            model_name='itemreview',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='itemreview',
            name='item',
        ),
        migrations.RemoveField(
            model_name='purchaseditem',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='purchaseditem',
            name='farmer',
        ),
        migrations.RemoveField(
            model_name='purchaseditem',
            name='item',
        ),
        migrations.DeleteModel(
            name='Buyer',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='Farmer',
        ),
        migrations.DeleteModel(
            name='FarmerItem',
        ),
        migrations.DeleteModel(
            name='ItemReview',
        ),
        migrations.DeleteModel(
            name='PurchasedItem',
        ),
        migrations.AddField(
            model_name='resume',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
        migrations.AddField(
            model_name='issue',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
        migrations.AddField(
            model_name='auctionbid',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.company'),
        ),
        migrations.AddField(
            model_name='application',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.job'),
        ),
        migrations.AddField(
            model_name='application',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.resume'),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
    ]
