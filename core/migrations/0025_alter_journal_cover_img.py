# Generated by Django 4.1.5 on 2023-02-19 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_alter_entry_created_at_alter_entry_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='cover_img',
            field=models.ImageField(default='images/blank-img.png', upload_to='images/'),
        ),
    ]
