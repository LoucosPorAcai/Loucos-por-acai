from django.conf.urls import include, url
from . import views


urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^cardapio/$', views.menu, name='menu'),
    url(r'^sobre/$', views.sobre, name='sobre'),
    url(r'^contato/$', views.contato, name='contato'),
    url(r'^login/$', views.login, name='login'),
    url(r'^cadastro_estoque/$', views.new_estoque, name='new_estoque'),
    url(r'^consulta_estoque/$', views.consulta_estoque, name='consulta_estoque'),
    url(r'^consulta_estoque/edicao/(?P<pk>[0-9]+)/$', views.edita_estoque, name='edita_estoque'),
    url(r'^consulta_estoque/deletar/(?P<id>[0-9]+)/$', views.delete_estoque, name='delete_estoque'),


]