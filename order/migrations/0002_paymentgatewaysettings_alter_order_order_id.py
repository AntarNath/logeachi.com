# Generated by Django 4.1.7 on 2023-09-25 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGateWaySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(blank=True, max_length=500, null=True)),
                ('store_pass', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='HzCdAsQFSh', editable=False, max_length=10, unique=True),
        ),
    ]
