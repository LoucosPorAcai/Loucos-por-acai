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
from datetime import datetime
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
            data={}
            data['userIsNone'] = True
            return render(request, 'view/login.html', data)
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
    data={}
    data['cliente'] = getClienteByUser(request.user)

    return render(request, 'view/perfil.html',data)

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
                cliente = Cliente.objects.get(usuario = usuario)
                funcionario = getFuncionarioByUser(request.user)
                carrinho = Carrinho.objects.create(valor_Total = 0)
                atendimento = Atendimento.objects.create(cliente = cliente, funcionario = funcionario,carrinho = carrinho)

                data['cliente'] = cliente
                data['atendimento'] = atendimento
                data['estoques'] = Estoque.objects.all()

                return render(request, 'view/venda.html', data)
            else:
                data['notIsCliente'] = True
                return render(request, 'view/venda.html', data)

        except Usuario.DoesNotExist:
            data['userIsNone'] = True
            return render(request, 'view/venda.html', data)
    else:
        return render(request, 'view/venda.html')

@login_required(login_url='/login/')
def lista_itens(request, cliente, atendimento, estoque=None):
    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    data = {}

    atendimento = Atendimento.objects.get(id=atendimento)
    cliente = Cliente.objects.get(id=cliente)
    carrinho = None
    query_estoque = request.POST.get('codigo')

    if query_estoque:

        estoque = Estoque.objects.filter(nome__contains = query_estoque)
        data['estoques'] = estoque

    else:
        nestoque = getProdutoById(estoque)
        nestoque.quant_produtos += 1
        nestoque.save()
        carrinho = atendimento.carrinho
        carrinho.estoque.add(nestoque)
        carrinho.valor_Total += nestoque.preco
        carrinho.save()
        data['estoques'] = Estoque.objects.all()

    data['cliente'] = cliente
    data['atendimento'] = atendimento
    data['carrinho'] = carrinho
    data['valor'] = carrinho.valor_Total

    return render(request,'view/venda.html', data)

@login_required(login_url='/login/')

def finalizar_compra(request,cliente,atendimento):
    if not request.user.has_perm('global_permissions.acessar_funcionario'):
        raise PermissionDenied
    atendimento = Atendimento.objects.get(id=atendimento)
    cliente = Cliente.objects.get(id=cliente)
    cartao = Cartao.objects.get(id= cliente.cartao.id)
    if atendimento.carrinho.valor_Total >= 7:
        for estoque in atendimento.carrinho.estoque.all():
            cartao.quant_pontos += (estoque.quant_produtos*estoque.pontos)
            cartao.save()
            cliente.save()
    for estoque in Estoque.objects.all():
        estoque.quant_produtos = 0
        estoque.save()
    atendimento.save()
    return HttpResponse('Compra finalizada com sucesso!')

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
    if request.method == "POST":

        cpf = request.POST.get('cpf_cliente')
        nome = request.POST.get('nome_cliente')
        snome = request.POST.get('sobrenome_cliente')
        email = request.POST.get('email_cliente')
        rua = request.POST.get('rua_cliente')
        numero = request.POST.get('numero_cliente')
        comp = request.POST.get('comp_cliente',False)
        bairro = request.POST.get('bairro_cliente')
        cep = request.POST.get('cep_cliente')
        cidade = request.POST.get('cidade_cliente')
        ddd1 = request.POST.get('ddd_cliente')
        telefone1 = request.POST.get('tel_cliente')
        ddd2 = request.POST.get('ddd2_cliente', False)
        telefone2 = request.POST.get('tel2_cliente', False)
        login = request.POST.get('login_cliente')
        senha = request.POST.get('senha_cliente')


        obj_telefone = Telefone.objects.create(ddd1 = ddd1, numero1 = telefone1, ddd2 = ddd2, numero2 = telefone2)
        obj_endereco = Endereco.objects.create(rua = rua, numero_casa = numero, complemento = comp, bairro = bairro, cep = cep, cidade = cidade)
        obj_user = User.objects.create_user(username = login, password = senha)
        gcliente = Group.objects.get(name='cliente')
        obj_user.groups.add(gcliente)
        obj_usuario = Usuario.objects.create(nome = nome, sobrenome = snome, email= email, cpf = cpf, endereco = obj_endereco, telefone = obj_telefone, user = obj_user )
        obj_telefone.save()
        obj_endereco.save()
        obj_user.save()
        obj_usuario.save()
        obj_cartao = Cartao.objects.create(quant_pontos = 0)
        obj_cartao.save()
        obj_cliente = Cliente.objects.create(usuario = obj_usuario, cartao = obj_cartao)
        obj_cliente.save()

        return HttpResponseRedirect('/funcionario/consulta_cliente/')
    else:
        return render(request, 'view/CadF.html')

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
    telefone = usuario.telefone
    endereco = usuario.endereco

    if request.method == "POST":

        usuario.cpf = request.POST.get('cpf_cliente')
        usuario.nome = request.POST.get('nome_cliente')
        usuario.sobrenome = request.POST.get('sobrenome_cliente')
        usuario.email = request.POST.get('email_cliente')
        endereco.rua = request.POST.get('rua_cliente')
        endereco.numero_casa = request.POST.get('numero_cliente')
        endereco.complemento= request.POST.get('comp_cliente')
        endereco.bairro = request.POST.get('bairro_cliente')
        endereco.cep = request.POST.get('cep_cliente')
        endereco.cidade = request.POST.get('cidade_cliente')
        telefone.ddd1 = request.POST.get('ddd_cliente')
        telefone.numero1 = request.POST.get('tel_cliente')
        telefone.ddd2 = request.POST.get('ddd2_cliente')
        telefone.numero2 = request.POST.get('tel2_cliente')

        telefone.save()
        endereco.save()
        usuario.save()
        cliente.save()

        return HttpResponseRedirect('/funcionario/consulta_cliente/')

    else:
        data['id'] = id
        data['cpf'] = usuario.cpf
        data['nome'] = usuario.nome
        data['snome'] = usuario.sobrenome
        data['email'] = usuario.email
        data['rua'] = endereco.rua
        data['numero'] = endereco.numero_casa
        data['comp'] = endereco.complemento
        data['bairro'] = endereco.bairro
        data['cep'] = endereco.cep
        data['cidade'] = endereco.cidade
        data['ddd1'] = telefone.ddd1
        data['telefone1'] = telefone.numero1
        data['ddd2'] = telefone.ddd2
        data['telefone2'] = telefone.numero2

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
def excluir_funcionario_gerente(request, pk):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    funcionario = Funcionario.objects.get(pk=pk)
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
    data={}

    atendimento = Atendimento.objects.all()
    cliente = Cliente.objects.all()
    funcionario = Funcionario.objects.all()

    data['atendimentos'] = atendimento
    data['clientes'] = cliente
    data['funcionarios'] = funcionario

    return render(request, 'view/consultarH.html',data)

@login_required(login_url='/login/')
def vendas_gerente(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    data = {}
    if request.method == 'POST':
        cpf = request.POST.get('CPF')
        try:
            usuario = getUsuarioByCpf(cpf)
            if usuario.isCliente():
                cliente = Cliente.objects.get(usuario=usuario)
                funcionario = getFuncionarioByUser(request.user)
                carrinho = Carrinho.objects.create(valor_Total=0)
                atendimento = Atendimento.objects.create(cliente=cliente, funcionario=funcionario, carrinho=carrinho)

                data['cliente'] = cliente
                data['atendimento'] = atendimento
                data['estoques'] = Estoque.objects.all()

                return render(request, 'view/vendaG.html', data)
            else:
                data['notIsCliente'] = True
                return render(request, 'view/vendaG.html', data)

        except Usuario.DoesNotExist:
            data['userIsNone'] = True
            return render(request, 'view/vendaG.html', data)
    else:
        return render(request, 'view/vendaG.html')

    return render(request, 'view/vendaG.html')

@login_required(login_url='/login/')
def lista_itens_gerente(request, cliente, atendimento, estoque=None):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    data = {}

    atendimento = Atendimento.objects.get(id=atendimento)
    cliente = Cliente.objects.get(id=cliente)
    carrinho = None
    query_estoque = request.POST.get('codigo')

    if query_estoque:

        estoque = Estoque.objects.filter(nome__contains = query_estoque)
        data['estoques'] = estoque

    else:
        nestoque = getProdutoById(estoque)
        nestoque.quant_produtos += 1
        nestoque.save()
        carrinho = atendimento.carrinho
        carrinho.estoque.add(nestoque)
        carrinho.valor_Total += nestoque.preco
        carrinho.save()
        data['estoques'] = Estoque.objects.all()

    data['cliente'] = cliente
    data['atendimento'] = atendimento
    data['carrinho'] = carrinho
    data['valor'] = carrinho.valor_Total

    return render(request,'view/vendaG.html', data)

@login_required(login_url='/login/')
def finalizar_compra_gerente(request,cliente,atendimento):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied
    atendimento = Atendimento.objects.get(id=atendimento)
    cliente = Cliente.objects.get(id=cliente)

    if atendimento.carrinho.valor_Total >= 7.00:
        for estoque in atendimento.carrinho.estoque.all():
            cliente.cartao.quant_pontos += estoque.pontos
            cliente.save()
    for estoque in Estoque.objects.all():
        estoque.quant_produtos = 0
        estoque.save()

    atendimento.save()
    return HttpResponse('Compra finalizada com sucesso!')

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
    estoque = Estoque.objects.get(pk=pk)

    if request.method == "POST":

        estoque.nome = request.POST.get('nome_estoque')
        estoque.quant_produtos = request.POST.get('quantidade_estoque')
        estoque.marca = request.POST.get('marca_estoque')
        estoque.preco = request.POST.get('preco_estoque')
        estoque.minimo = request.POST.get('limite_estoque')
        estoque.pontos = request.POST.get('ponto_estoque')
        estoque.save()

        return HttpResponseRedirect('/gerente/consulta_estoque/')

    else:
        data['pk'] = pk
        data['nome'] = estoque.nome
        data['quantidade'] = estoque.quant_produtos
        data['marca'] = estoque.marca
        data['preco'] = estoque.preco
        data['minimo'] = estoque.minimo
        data['pontos'] = estoque.pontos

        return render(request, 'view/editeEdicaoE.html', data)

@login_required(login_url='/login/')
def new_estoque(request):
    if not request.user.has_perm('global_permissions.acessar_gerente'):
        raise PermissionDenied

    if request.method == "POST":

        nome = request.POST.get('nome_estoque')
        quant = request.POST.get('quantidade_estoque')
        marca = request.POST.get('marca_estoque')
        preco = request.POST.get('preco_estoque')
        minimo = request.POST.get('limite_estoque')
        pontos = request.POST.get('ponto_estoque', False)

        if pontos:
            obj_estoque = Estoque.objects.create(nome=nome, marca=marca, preco=preco, quant_produtos=quant,minimo=minimo,pontos=pontos)

        else:

            obj_estoque = Estoque.objects.create(nome=nome, marca=marca, preco=preco, quant_produtos=quant, minimo=minimo)

        obj_estoque.save()

        return HttpResponseRedirect('/gerente/consulta_estoque/')

    else:
        return render(request, 'view/cadE.html')
