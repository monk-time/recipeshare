# Generated by Django 4.2.4 on 2023-08-12 09:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0003_alter_ingredient_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={
                'ordering': ('name',),
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
    ]
