from django.contrib import admin
from .models import Estoque
from .models import Endereco
from .models import Telefone
from .models import Usuario
from .models import Cartao
from .models import Cliente
from .models import Situacao
from .models import Tipofuncionario
from .models import Funcionario
from .models import Atendimento
from .models import Carrinho
from .models import Trocapontos

#Registros

admin.site.register(Estoque)
admin.site.register(Endereco)
admin.site.register(Telefone)
admin.site.register(Usuario)
admin.site.register(Cartao)
admin.site.register(Cliente)
admin.site.register(Situacao)
admin.site.register(Tipofuncionario)
admin.site.register(Funcionario)
admin.site.register(Atendimento)
admin.site.register(Carrinho)
admin.site.register(Trocapontos)







