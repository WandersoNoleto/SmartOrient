# Generated by Django 4.2.6 on 2023-11-06 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='Nome Completo')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('enrollment', models.CharField(max_length=50, verbose_name='Matrícula')),
                ('phone_number', models.CharField(max_length=50, verbose_name='Número de Telefone')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='Nome Completo')),
                ('course', models.CharField(max_length=50, verbose_name='Curso')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('enrollment', models.CharField(max_length=50, verbose_name='Matrícula')),
                ('phone_number', models.CharField(max_length=50, verbose_name='Número de Telefone')),
            ],
        ),
    ]
