# Generated by Django 2.2 on 2019-04-14 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0006_auto_20190414_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='standing_capacity',
            field=models.PositiveIntegerField(default=3100),
        ),
    ]