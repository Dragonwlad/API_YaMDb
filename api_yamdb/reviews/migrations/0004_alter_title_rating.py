# Generated by Django 4.0 on 2023-08-02 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.DecimalField(decimal_places=0, default=None, max_digits=2, null=True),
        ),
    ]