from django.conf.urls import include, url
from . import views


urlpatterns = [

    url(r'^$', views.new_estoque, name='new_estoque'),
    url(r'^consulta_estoque/$', views.consulta_estoque, name='consulta_estoque'),
    url(r'^consulta_estoque/edicao/(?P<pk>[0-9]+)/$', views.edita_estoque, name='edita_estoque'),
    url(r'^consulta_estoque/deletar/(?P<id>[0-9]+)/$', views.delete_estoque, name='delete_estoque'),



]