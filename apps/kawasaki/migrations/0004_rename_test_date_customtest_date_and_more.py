# Generated by Django 5.2.4 on 2025-07-09 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kawasaki', '0003_rename_othertest_infectioustest_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customtest',
            old_name='test_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='customtest',
            old_name='test_name',
            new_name='name',
        ),
    ]
