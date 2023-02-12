# Generated by Django 4.1.5 on 2023-02-12 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_entry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='image',
        ),
        migrations.AlterField(
            model_name='entry',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='core.image'),
        ),
    ]
