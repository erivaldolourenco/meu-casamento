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
    cpf = models.CharField(max_length=15)
    email = models.EmailField()
    presente = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateField()

    def __str__(self):
        return self.nome