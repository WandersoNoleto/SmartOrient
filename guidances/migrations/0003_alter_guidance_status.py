# Generated by Django 4.2.6 on 2023-11-16 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guidances', '0002_alter_guidance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidance',
            name='status',
            field=models.CharField(default='Pendente', max_length=50, verbose_name='Status'),
        ),
    ]