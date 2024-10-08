# Generated by Django 5.0.6 on 2024-09-15 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listapresente', '0003_produto_descricao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comprador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('sobrenome', models.CharField(max_length=200)),
                ('cpf', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=15)),
            ],
        ),
    ]
