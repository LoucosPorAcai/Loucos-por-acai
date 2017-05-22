from django.conf.urls import include, url
from . import views


urlpatterns = [

    url(r'^$', views.index_gerente, name='index'),
    url(r'^cardapio/$', views.menu, name='menu'),
    url(r'^sobre/$', views.sobre, name='sobre'),
    url(r'^contato/$', views.contato, name='contato'),
    url(r'^login/$', views.login, name='login'),
    url(r'^cliente/$', views.index_cliente, name='indexCliente'),
    url(r'^cliente/cardapio/$', views.menu_cliente, name='cardapioCliente'),
    url(r'^cliente/sobre/$', views.sobre_cliente, name='sobreNosCliente'),
    url(r'^cliente/contato/$', views.contato_cliente, name='contatoCliente'),
    url(r'^cliente/perfil/$', views.perfil_cliente, name='perfil'),
    url(r'^cliente/perfil/editar/$', views.editar_cliente, name='editeEdicao'),
    url(r'^funcionario/$', views.index_funcionario, name='indexFunc'),
    url(r'^funcionario/cardapio/$', views.menu_funcionario, name='cardapioFunc'),
    url(r'^funcionario/sobre/$', views.sobre_funcionario, name='sobreNosFunc'),
    url(r'^funcionario/contato/$',views.contato_funcionario, name='contatoFunc'),
    url(r'^funcionario/venda/$', views.vendas_funcionario, name='vendas'),
    url(r'^funcionario/cadastro_cliente/$', views.new_cliente, name='cadastroFunc'),
    url(r'^funcionario/consulta_cliente/$', views.consultar_cliente, name='consultaC'),
    url(r'^funcionario/editar_cliente/$', views.editar_cliente_funcionario, name='editeEdicaoCliente'),
    url(r'^funcionario/editar/$', views.editar_funcionario, name='editeEdicaoFunc'),
    url(r'^gerente/index/$', views.index_gerente, name='indexGeren'),
    url(r'^gerente/menu/$', views.menu_gerente, name='cardapioGeren'),
    url(r'^gerente/sobre/$', views.sobre_gerente, name='sobreNosGeren'),
    url(r'^gerente/contato/$', views.contato_gerente, name='contatoGeren'),
    url(r'^gerente/cadastro_funcionario/$',views.new_funcionario, name='cadastroGeren'),
    url(r'^gerente/consultar_funcionario/$', views.consultar_funcionario, name='consultarFunc'),
    url(r'^gerente/consultar_funcionario/editar_funcionario/(?P<id>[0-9]+)$', views.editar_funcionario_gerente, name='editarFuncionario'),
    url(r'^gerente/consultar_funcionario/excluir_funcionario/(?P<id>[0-9]+)$', views.excluir_funcionario_gerente, name='excluirFuncionario'),
    url(r'^gerente/consultar_historico/$', views.consultar_historico, name='consultarHistor'),
    url(r'^gerente/venda/$', views.vendas_gerente, name='vendasGeren'),
    url(r'^gerente/cadastro_estoque/$', views.new_estoque, name='cadastroEstoque'),
    url(r'^gerente/consulta_estoque/$', views.consulta_estoque, name='consulta_estoque'),
    url(r'^gerente/consulta_estoque/edicao/(?P<pk>[0-9]+)/$', views.edita_estoque, name='edita_estoque'),
    url(r'^gerente/consulta_estoque/deletar/(?P<id>[0-9]+)/$', views.delete_estoque, name='delete_estoque'),


]