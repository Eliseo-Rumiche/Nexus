# Generated by Django 5.0.4 on 2024-05-26 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worker",
            name="phone_number",
            field=models.CharField(
                help_text="Ejm : +51 963852741",
                max_length=50,
                verbose_name="Número de Teléfono",
            ),
        ),
    ]