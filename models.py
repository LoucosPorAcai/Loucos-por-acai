# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Atendimento(models.Model):

    id = models.IntegerField(primary_key=True)
    tipo_entrega = models.CharField(max_length=45)
    data = models.DateField('Data do Atendimento')
    hora = models.CharField(max_length=45)

    FK_atendimento_funcionario = models.ForeignKey(Funcionario, blank=True, null=False)
    FK_atendimento_cliente = models.ForeignKey(Cliente, blank=True, null=False)

    class Meta:
        db_table = 'atendimento'

class Carrinho(models.Model):

    FK_carrinho_estoque = models.ForeignKey(Estoque, blank=True, null=False)
    FK_carrinho_atendimento = models.ForeignKey(Atendimento,blank=True, null=False)

    class Meta:
        db_table = 'carrinho'


class Cartao(models.Model):

    id = models.IntegerField(primary_key=True)  # AutoField?
    quant_pontos = models.IntegerField()

    class Meta:
        db_table = 'cartao'

class Cliente(models.Model):

    id = models.IntegerField(primary_key=True)

    FK_cliente_usuario = models.ForeignKey(Usuario, blank=True, null=False)
    FK_cliente_cartao = models.ForeignKey(Cartao, blank=True, null=False)

    class Meta:
        db_table = 'cliente'

class Endereco(models.Model):

    id = models.IntegerField(primary_key=True)  # AutoField?
    rua = models.CharField(max_length=100)
    numero_casa = models.IntegerField()
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cep = models.IntegerField()
    cidade = models.CharField(max_length=100)

    class Meta:
        db_table = 'endereco'


class Estoque(models.Model):

    id = models.IntegerField(primary_key=True)  # AutoField?
    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    preco = models.TextField()  # This field type is a guess.
    quant_produtos = models.CharField(max_length=45)
    minimo = models.IntegerField()
    pontos = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'estoque'

class Funcionario (models.Model):

    id = models.IntegerField(primary_key=True)
    salario = models.FloatField()
    periodo_trabalho = models.CharField(max_length=45)

    FK_funcionario_usuario = models.ForeignKey(Usuario, blank=True, null=False)
    FK_funcionario_tipo_funcionario = models.ForeignKey(Tipofuncionario ,blank=True , null=False)
    FK_funcionario_situacao = models.ForeignKey(Situacao, blank=True, null=False)

    class Meta:
        db_table = 'funcionario'

class Situacao(models.Model):

    id = models.IntegerField(primary_key=True)  # AutoField?
    descricao = models.CharField(max_length=45)

    class Meta:
        db_table = 'situacao'


class Telefone(models.Model):

    id = models.IntegerField(primary_key=True)  # AutoField?
    ddd1 = models.IntegerField()
    numero1 = models.CharField(max_length=15)
    ddd2 = models.IntegerField(blank=True, null=True)
    numero2 = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'telefone'


class Tipofuncionario(models.Model):

    id = models.IntegerField(primary_key=True)  # AutoField?
    desc_tipo = models.CharField(max_length=45)

    class Meta:
        db_table = 'tipoFuncionario'

class Trocapontos(models.Model):

    id = models.IntegerField(primary_key=True)
    pontos_gastos = models.IntegerField()
    data = models.DateField('Data da troca')
    hora = models.CharField(max_length=45)
    FK_trocaPontos_funcionario = models.ForeignKey(Funcionario, blank=True, null=False)
    FK_trocaPontos_cliente = models.ForeignKey(Cliente,blank=True,null=False)
    FK_trocaPontos_estoque = models.ForeignKey(Estoque,blank=True,null=False)

    class Meta:
        db_table = 'trocapontos'

class Usuario(models.Model):

    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=45)
    sobrenome = models.CharField(max_length=45)
    cpf = models.CharField(max_length=14)
    login = models.CharField(max_length=45)
    senha = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    FK_usuario_endereco = models.ForeignKey(Endereco,blank=True, null=False)
    FK_usuario_telefone = models.ForeignKey(Telefone, blank=True, null=False)


    class Meta:
        db_table = 'usuario'