from django import forms
from .models import Estoque
from .models import Funcionario
from .models import Usuario
from .models import Telefone
from .models import Endereco
from .models import Tipofuncionario
from .models import Situacao

class EstoqueForm(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = ('nome','marca','preco','quant_produtos','minimo','pontos',)

class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ('salario','periodo_trabalho','usuario','tipo_funcionario','situacao',)
class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('nome','sobrenome','cpf','login','senha','email','endereco','telefone',)

class TelefoneForm(forms.ModelForm):

    class Meta:
        model = Telefone
        fields = ('ddd1','numero1','ddd2','numero2',)

class EnderecoForm(forms.ModelForm):

    class Meta:

        model = Endereco
        fields = ('rua','numero_casa','complemento','bairro','cep','cidade',)

class TipofuncionarioForm(forms.ModelForm):

    class Meta:

        model = Tipofuncionario
        fields = ('desc_tipo',)

class SituacaoForm(forms.ModelForm):

    class Meta:

        model = Situacao
        fields = ('descricao',)
