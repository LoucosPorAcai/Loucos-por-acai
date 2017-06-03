#_*_coding:latin-1_*_
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from .forms import *
from .models import *

from django.contrib import messages

def index(request):
    return render(request, 'view/index.html')

def index_redirect(request):
    return HttpResponseRedirect('home/')

def menu(request):
    return render(request, 'view/cardapio.html')

def sobre(request):
    return render(request, 'view/sobreNos.html')

def contato(request):
    return render(request, 'view/contato.html')

def logar(request):

    if request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(username=usuario, password=senha)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.username == 'admin':
                    return HttpResponseRedirect('/admin/')
                for group in user.groups.all():
                    if group.name == 'cliente':
                        return HttpResponseRedirect('/cliente/')
                    elif group.name == 'funcionario':
                        return HttpResponseRedirect('/funcionario/')
                    elif group.name == 'gerente':
                        return HttpResponseRedirect('/gerente/')
        else:
            return HttpResponse('usuário não encontrado')
    else:
        return render(request, 'view/login.html')

@login_required(login_url='/login/')
def deslogar(request):
    logout(request)
    return HttpResponseRedirect('/home/')

@login_required(login_url='/login/')
def index_cliente(request):
    if not request.user.has_perm('global_permissions.acessar_cliente'):
        raise PermissionDenied
    return render(request, 'view/indexC.html')

@login_required(login_url='/login/')
def menu_cliente(request):
    if not request.user.has_perm('global_permissions.acessar_cliente'):
        raise PermissionDenied
    return render(request, 'view/cardapioC.html')

@login_required(login_url='/login/')
def sobre_cliente(request):
    if not request.user.has_perm('global_permissions.acessar_cliente'):
        raise PermissionDenied
    return render(request, 'view/sobreNosC.html')

@login_required(login_url='/login/')
def contato_cliente(request):
    if not request.user.has_perm('global_permissions.acessar_cliente'):
        raise PermissionDenied
    return render(request, 'view/contatoC.html')

@login_required(login_url='/login/')
def perfil_cliente(request):
    if not request.user.has_perm('global_permissions.acessar_cliente'):
        raise PermissionDenied
    return render(request, 'view/perfil.html')

@login_required(login_url='/login/')
def editar_cliente(request):
    if not request.user.has_perm('global_permissions.acessar_cliente'):
        raise PermissionDenied

    return render(request, 'view/editeEdicao.html')

@login_required(login_url='/login/')
def index_funcionario(request):
    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    return render(request, 'view/indexF.html')

@login_required(login_url='/login/')
def menu_funcionario(request):
    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    return  render(request, 'view/cardapioF.html')

@login_required(login_url='/login/')
def sobre_funcionario(request):
    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    return  render(request, 'view/sobreNosF.html')

@login_required(login_url='/login/')
def contato_funcionario(request):
    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    return render(request, 'view/contatoF.html')

@login_required(login_url='/login/')
def vendas_funcionario(request):
    data={}

    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    if request.method == 'POST':
        cpf = request.POST.get('CPF')
        try:
            usuario = getUsuarioByCpf(cpf)
            if usuario.isCliente():
                telefone = usuario.telefone
                endereco = usuario.endereco
                data['cpf'] = usuario.cpf
                data['nome'] = usuario.nome
                data['ddd1'] = telefone.ddd1
                data['numero1'] = telefone.numero1
                data['rua'] = endereco.rua
                data['numero'] = endereco.numero_casa
                data['complemento'] = endereco.complemento
                data['bairro'] = endereco.bairro
                data['cidade'] = endereco.cidade
                return render(request, 'view/venda.html', data)
            else:
                return HttpResponse("Usuário não é cliente")

        except Usuario.DoesNotExist:
            return HttpResponse("Usuário não existe")
    else:
        return render(request, 'view/venda.html')

@login_required(login_url='/login/')
def delete_estoque(request,id):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    estoque = Estoque.objects.filter(id=id)
    estoque.delete()
    return HttpResponseRedirect('/gerente/consulta_estoque/')

@login_required(login_url='/login/')
def new_cliente(request):
    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    data = {}
    if request.method == "POST":

        cliform = ClienteForm(request.POST)
        usrform = UsuarioForm(request.POST)
        cartaoform = CartaoForm(request.POST)
        endform = EnderecoForm(request.POST)
        telform = TelefoneForm(request.POST)
        userform = UserCreationForm(request.POST)
        if telform.is_valid() and cartaoform.is_valid()and endform.is_valid() and all(userform.is_valid() for user in userform) and all(
                [usrform.is_valid() for usr in usrform]) and all([cliform.is_valid() for cli in cliform]):

            new_telefone = telform.save()
            new_cartao = cartaoform.save()
            new_end = endform.save()
            for user in userform:
                new_user_auth = userform.save(commit=False)
                gcliente = Group.objects.get(name='cliente')
                new_user_auth.save()
                new_user_auth.groups.add(gcliente)
                for usr in usrform:
                    new_user = usrform.save(commit=False)
                    new_user.telefone = new_telefone
                    new_user.endereco = new_end
                    new_user.user = new_user_auth
                    new_user.save()
                    for cli in cliform:
                        new_cli = cliform.save(commit=False)
                        new_cli.cartao = new_cartao
                        new_cli.usuario = new_user
                        new_cli.save()
                    return HttpResponseRedirect('/funcionario/consulta_cliente/')
    else:
        cliform = ClienteForm()
        usrform = UsuarioForm()
        cartaoform = CartaoForm()
        endform = EnderecoForm()
        telform = TelefoneForm()
        userform = UserCreationForm()

    data['clientes'] = cliform
    data['usuarios'] = usrform
    data['cartoes'] = cartaoform
    data['enderecos'] = endform
    data['telefones'] = telform
    data['user'] = userform

    return render(request, 'view/CadF.html', data)

@login_required(login_url='/login/')
def consultar_cliente(request):
    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    data = {}
    data['clientes'] = Cliente.objects.all()
    data['usuarios'] = Usuario.objects.all()

    return render(request, 'view/ConsultarCF.html',data)

@login_required(login_url='/login/')
def editar_cliente_funcionario(request,id):
    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    data = {}
    cliente = Cliente.objects.get(pk=id)
    usuario = cliente.usuario

    if request.method == "POST":

        cliform = ClienteForm(request.POST, instance=cliente)
        usrform = UsuarioForm(request.POST, instance=usuario)
        cartaoform = CartaoForm(request.POST, instance=cliente.cartao)
        endform = EnderecoForm(request.POST, instance=usuario.endereco)
        telform = TelefoneForm(request.POST, instance=usuario.telefone)
        userform = UserCreationForm(request.POST, instance=usuario.user)

        if telform.is_valid() and cartaoform.is_valid() and userform.is_valid() and endform.is_valid() and all(
                [usrform.is_valid() for usr in usrform]) and all([cliform.is_valid() for cli in cliform]):

            new_telefone = telform.save()
            new_cartao = cartaoform.save()
            new_end = endform.save()
            new_user_auth = userform.save()

            for usr in usrform:
                new_user = usrform.save(commit=False)
                new_user.telefone = new_telefone
                new_user.endereco = new_end
                new_user.user = new_user_auth
                new_user.save()
                for cli in cliform:
                    new_cli = cliform.save(commit=False)
                    new_cli.cartao = new_cartao
                    new_cli.usuario = new_user
                    new_cli.save()
                return HttpResponseRedirect('/funcionario/consulta_cliente/')

    else:
        cliform = ClienteForm(instance=cliente)
        usrform = UsuarioForm(instance=usuario)
        cartaoform = CartaoForm(instance=cliente.cartao)
        endform = EnderecoForm(instance=usuario.endereco)
        telform = TelefoneForm(instance=usuario.telefone)
        userform = UserCreationForm(instance=usuario.user)

    data['clientes'] = cliform
    data['usuarios'] = usrform
    data['cartoes'] = cartaoform
    data['enderecos'] = endform
    data['telefones'] = telform
    data['user'] = userform

    return render(request, 'view/editeEdicaoF.html', data)

@login_required(login_url='/login/')
def excluir_cliente(request, id):
    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    cliente = Cliente.objects.get(pk=id)
    usuario = cliente.usuario
    cartao = cliente.cartao
    telefone = usuario.telefone
    endereco = usuario.endereco
    user = usuario.user

    endereco.delete()
    telefone.delete()
    cartao.delete()
    user.delete()
    usuario.delete()
    cliente.delete()

    return HttpResponseRedirect('/funcionario/consulta_cliente/')

@login_required(login_url='/login/')
def index_gerente(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    return render(request, 'view/indexG.html')

@login_required(login_url='/login/')
def menu_gerente(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    return render(request, 'view/cardapioG.html')

@login_required(login_url='/login/')
def sobre_gerente(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    return render(request, 'view/sobreNosG.html')

@login_required(login_url='/login/')
def contato_gerente(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    return render(request, 'view/contatoG.html')

@login_required(login_url='/login/')
def new_funcionario(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    data = {}

    if request.method == "POST":
        funcform = FuncionarioForm(request.POST)
        usrform = UsuarioForm(request.POST)
        tpfuncform = TipofuncionarioForm(request.POST)
        endform = EnderecoForm(request.POST)
        sform = SituacaoForm(request.POST)
        telform = TelefoneForm(request.POST)
        userform = UserCreationForm(request.POST)

        if telform.is_valid() and sform.is_valid() and endform.is_valid() and userform.is_valid() and tpfuncform.is_valid() and sform.is_valid() and all([usrform.is_valid() for usr in usrform]) and all([funcform.is_valid() for func in funcform]):
            new_telefone = telform.save()
            new_tipo = tpfuncform.save()
            new_end = endform.save()
            new_situacao = sform.save()
            new_user_auth = userform.save()

            if new_situacao.descricao == 'A':
                new_user_auth.is_active = True
            else:
                new_user_auth.is_active = False

            if new_tipo.desc_tipo == 'F':
                gfunc = Group.objects.get(name='funcionario')
            else:
                gfunc = Group.objects.get(name='gerente')
            new_user_auth.groups.add(gfunc)

            for usr in usrform:
                new_user = usrform.save(commit=False)
                new_user.telefone = new_telefone
                new_user.endereco = new_end
                new_user.user = new_user_auth
                new_user.save()
                for func in funcform:
                    new_func = funcform.save(commit=False)
                    new_func.situacao = new_situacao
                    new_func.tipo_funcionario = new_tipo
                    new_func.usuario = new_user
                    new_func.save()
                return HttpResponseRedirect('/gerente/consultar_funcionario/')
    else:
        funcform = FuncionarioForm()
        usrform = UsuarioForm()
        tpfuncform = TipofuncionarioForm()
        endform = EnderecoForm()
        sform = SituacaoForm()
        telform = TelefoneForm()
        userform = UserCreationForm()

    data['funcionarios'] = funcform
    data['usuarios'] = usrform
    data['tipos'] = tpfuncform
    data['enderecos'] = endform
    data['situacoes'] = sform
    data['telefones'] = telform
    data['user'] = userform

    return render(request, 'view/cadG.html', data)

@login_required(login_url='/login/')
def consultar_funcionario(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    data = {}
    data['funcionarios'] = Funcionario.objects.all()
    data['usuarios'] = Usuario.objects.all()
    return render(request, 'view/ConsultarF.html', data)

@login_required(login_url='/login/')
def editar_funcionario_gerente(request, id):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    data = {}
    funcionario = Funcionario.objects.get(pk=id)
    usuario = funcionario.usuario
    old_user = usuario.user

    if request.method == "POST":

        funcform = FuncionarioForm(request.POST, instance=funcionario)
        usrform = UsuarioForm(request.POST, instance=usuario)
        tpfuncform = TipofuncionarioForm(request.POST, instance=funcionario.tipo_funcionario)
        endform = EnderecoForm(request.POST, instance=usuario.endereco)
        sform = SituacaoForm(request.POST, instance=funcionario.situacao)
        telform = TelefoneForm(request.POST, instance=usuario.telefone)

        if telform.is_valid() and sform.is_valid() and endform.is_valid() and tpfuncform.is_valid() and sform.is_valid() and all(
                [usrform.is_valid() for usr in usrform])and all([funcform.is_valid() for func in funcform]):

            old_user.groups.clear()
            new_telefone = telform.save()
            new_tipo = tpfuncform.save()
            new_end = endform.save()
            new_situacao = sform.save()

            if new_tipo.desc_tipo == 'F':
                gfunc = Group.objects.get(name='funcionario')
            else:
                gfunc = Group.objects.get(name='gerente')

            old_user.groups.add(gfunc)

            for usr in usrform:
                new_user = usrform.save(commit=False)
                new_user.telefone = new_telefone
                new_user.endereco = new_end
                new_user.user = old_user
                new_user.save()

                for func in funcform:
                    new_func = funcform.save(commit=False)
                    new_func.situacao = new_situacao
                    new_func.tipo_funcionario = new_tipo
                    new_func.usuario = new_user
                    new_func.save()

                return HttpResponseRedirect('/gerente/consultar_funcionario/')

    else:
        funcform = FuncionarioForm(instance=funcionario)
        usrform = UsuarioForm(instance=usuario)
        tpfuncform = TipofuncionarioForm(instance=funcionario.tipo_funcionario)
        endform = EnderecoForm(instance=usuario.endereco)
        sform = SituacaoForm(instance=funcionario.situacao)
        telform = TelefoneForm(instance=usuario.telefone)


    data['funcionarios'] = funcform
    data['usuarios'] = usrform
    data['tipos'] = tpfuncform
    data['enderecos'] = endform
    data['situacoes'] = sform
    data['telefones'] = telform

    return render(request, 'view/editeEdicaoG.html', data)

@login_required(login_url='/login/')
def excluir_funcionario_gerente(request, id):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    funcionario = Funcionario.objects.get(pk=id)
    usuario = funcionario.usuario
    tipo = funcionario.tipo_funcionario
    situacao = funcionario.situacao
    telefone = usuario.telefone
    endereco = usuario.endereco
    user = usuario.user
    user.groups.clear()

    endereco.delete()
    telefone.delete()
    situacao.delete()
    tipo.delete()
    user.delete()
    usuario.delete()
    funcionario.delete()
    return HttpResponseRedirect('/gerente/consultar_funcionario/')

@login_required(login_url='/login/')
def consultar_historico(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    return render(request, 'view/consultarH.html')

@login_required(login_url='/login/')
def vendas_gerente(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    return render(request, 'view/vendaG.html')

@login_required(login_url='/login/')
def consulta_estoque(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    data = {}
    data['estoques'] = Estoque.objects.all()
    return render(request,'view/ConsultarE.html',data)

@login_required(login_url='/login/')
def edita_estoque(request,pk):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    data = {}
    estoque = get_object_or_404(Estoque, pk=pk)

    if request.method == "POST":
        form = EstoqueForm(request.POST, instance=estoque)

        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/gerente/consulta_estoque/')
    else:
        form = EstoqueForm(instance=estoque)

    data['form'] = form
    return render(request, 'view/editeEdicaoE.html', data)

@login_required(login_url='/login/')
def new_estoque(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    data = {}

    if request.method == "POST":
        form = EstoqueForm(request.POST)

        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/gerente/consulta_estoque/')
    else:
        form = EstoqueForm()

    data['form'] = form

    return render(request, 'view/cadE.html', data)

