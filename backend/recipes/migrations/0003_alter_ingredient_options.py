# Generated by Django 4.2.4 on 2023-08-08 21:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={
                'ordering': ('id',),
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
    ]