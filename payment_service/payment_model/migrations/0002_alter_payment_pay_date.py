# Generated by Django 4.2.1 on 2023-05-07 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment_model", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="pay_date",
            field=models.CharField(max_length=100),
        ),
    ]
