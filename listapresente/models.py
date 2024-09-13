from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos',null=True, blank=True)


    def __str__(self):
        return self.nome

class Comprador(models.Model):
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=15)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    def __str__(self):
        return self.nome