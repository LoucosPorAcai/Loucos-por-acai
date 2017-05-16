from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Estoque
from .models import Funcionario
from .models import Usuario
from .models import Endereco
from .models import Telefone
from .forms import EstoqueForm
from .forms import FuncionarioForm
from django.contrib import messages

def index(request):
    return render(request, 'view/index.html')

def menu(request):
    return render(request, 'view/cardapio.html')

def sobre(request):
    return render(request, 'view/sobreNos.html')

def contato(request):
    return render(request, 'view/contato.html')

def login(request):
    return render(request, 'view/login.html')

def index_cliente(request):
    return render(request, 'view/indexC.html')

def menu_cliente(request):
    return render(request, 'view/cardapioC.html')

def sobre_cliente(request):
    return render(request, 'view/sobreNosC.html')

def contato_cliente(request):
    return render(request, 'view/contatoC.html')

def perfil_cliente(request):
    return render(request, 'view/perfil.html')

def consultar_cliente(request):
    return render(request, 'view/ConsultarCF.html')

def index_funcionario(request):
    return render(request, 'view/indexF.html')

def menu_funcionario(request):
    return  render(request, 'view/cardapioF.html')

def sobre_funcionario(request):
    return  render(request, 'view/sobreNosF.html')

def contato_funcionario(request):
    return render(request, 'view/contatoF.html')

def vendas_funcionario(request):
    return render(request, 'view/venda.html')

def delete_estoque(request,id):

    estoque = Estoque.objects.filter(id=id)
    estoque.delete()
    return HttpResponseRedirect("/consulta/")

def editar_funcionario(request):
    return render(request, 'view/editeEdicaoF.html')

def new_cliente(request):
    return render(request, 'view/cadF.html')

def editar_cliente_funcionario(request):
    return render(request, 'view/editeEdicaoF.html')

def index_gerente(request):
    return render(request, 'view/indexG.html')

def menu_gerente(request):
    return render(request, 'view/cardapioG.html')

def sobre_gerente(request):
    return render(request, 'view/sobreNosG.html')

def contato_gerente(request):
    return render(request, 'view/contatoG.html')

def new_funcionario(request,id):
    data = {}

    if request.method == "POST":
        data['cpf'] = request.POST.get('cpf')
    else:
        form = FuncionarioForm()
    data['form'] = form
    return render(request, 'view/cadG.html', data)

def consultar_funcionario(request):

    data = {}
    data['funcionarios'] = Funcionario.objects.all()
    data['usuarios'] = Usuario.objects.all()
    return render(request, 'view/ConsultarF.html', data)

def editar_funcionario_gerente(request):
    return render(request, 'view/editeEdicaoG.html')

def consultar_historico(request):
    return render(request, 'view/consultarH.html')

def vendas_gerente(request):
    return render(request, 'view/vendaG.html')

def consulta_estoque(request):
    data = {}
    data['estoques'] = Estoque.objects.all()
    return render(request,'view/editar.html',data)

def edita_estoque(request,pk):

    data = {}
    estoque = get_object_or_404(Estoque, pk=pk)

    if request.method == "POST":
        form = EstoqueForm(request.POST, instance=estoque)

        if form.is_valid():
            form.save()
    else:
        form = EstoqueForm(instance=estoque)

    data['form'] = form

    return render(request, 'view/editeEdicaoG.html', data)


def new_estoque(request):
    data = {}

    if request.method == "POST":
        form = EstoqueForm(request.POST)

        if form.is_valid():
            form.save()
    else:
        form = EstoqueForm()

    data['form'] = form

    return render(request, 'view/cadG.html', data)

