# Generated by Django 4.0.4 on 2022-07-12 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='questiom_text',
            new_name='questiontext',
        ),
    ]