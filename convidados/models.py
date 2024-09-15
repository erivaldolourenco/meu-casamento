from django.db import models

# Create your models here.


class Convidado(models.Model):
    nome = models.CharField(max_length=100)
    presenca_confirmada = models.BooleanField(default=False)
    def __str__(self):
        return self.nome

class Acompanhante(models.Model):
    nome = models.CharField(max_length=100)
    convidado = models.ForeignKey(Convidado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class ConvidadoPresente(models.Model):
    nome_convidado = models.CharField(max_length=100)
    sobrenome_convidado = models.CharField(max_length=100)
    id_pagamento = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    produto_nome = models.CharField(max_length=100)
    produto_descricao = models.TextField()
    valor_recebido = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    data_compra = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_convidado