# Generated by Django 5.1.2 on 2024-12-10 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0003_invoice_course_invoice_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetype',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
