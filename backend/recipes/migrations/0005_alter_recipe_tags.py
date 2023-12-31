# Generated by Django 4.2.4 on 2023-09-22 10:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0004_alter_ingredient_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(
                related_name='recipes',
                to='recipes.tag',
                verbose_name='Список тегов',
            ),
        ),
    ]
