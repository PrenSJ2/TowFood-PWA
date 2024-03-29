# Generated by Django 4.0.4 on 2022-08-18 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Larder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('addressFirstLine', models.CharField(max_length=500)),
                ('postCode', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('addressFirstLine', models.CharField(max_length=500)),
                ('ageGroup', models.CharField(max_length=100)),
                ('ethnicity', models.CharField(max_length=100)),
                ('postCode', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('prefContact', models.CharField(max_length=100)),
                ('occupation', models.CharField(max_length=100)),
                ('isCarer', models.BooleanField(default=False)),
                ('isMember', models.BooleanField(default=True)),
                ('isEmployed', models.BooleanField(default=True)),
                ('noAdults', models.IntegerField(default=0)),
                ('noChildren', models.IntegerField(default=0)),
                ('foodAllergies', models.CharField(max_length=300)),
                ('acceptedPolicy', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('totalFoodCollected', models.FloatField(default=0)),
                ('baselineHealthScore', models.FloatField(default=0)),
                ('currentHealthScore', models.FloatField(default=0)),
                ('prefLarder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.larder')),
            ],
        ),
        migrations.CreateModel(
            name='Pickup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('larder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.larder')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.member')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('barcode', models.IntegerField()),
                ('category', models.CharField(max_length=500)),
                ('perishable', models.BooleanField(default=False)),
                ('allergens', models.CharField(max_length=500)),
                ('weight', models.FloatField(default=0)),
                ('quantity', models.IntegerField(default=1)),
                ('footprint', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.collection')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('addressFirstLine', models.CharField(max_length=500)),
                ('postCode', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('addressFirstLine', models.CharField(max_length=500)),
                ('postCode', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('isAdmin', models.BooleanField(default=False)),
                ('age', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('prefLarder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.larder')),
            ],
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('larder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.larder')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.member')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOut',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('barcode', models.IntegerField()),
                ('category', models.CharField(max_length=500)),
                ('perishable', models.BooleanField(default=False)),
                ('allergens', models.CharField(max_length=500)),
                ('weight', models.FloatField(default=0)),
                ('quantity', models.IntegerField(default=1)),
                ('footprint', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pickup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.pickup')),
            ],
        ),
        migrations.AddField(
            model_name='pickup',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.volunteer'),
        ),
        migrations.AddField(
            model_name='collection',
            name='larder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.larder'),
        ),
        migrations.AddField(
            model_name='collection',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.supplier'),
        ),
        migrations.AddField(
            model_name='collection',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.volunteer'),
        ),
    ]
