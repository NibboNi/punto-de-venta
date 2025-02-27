from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/negocios/', views.business, name='business'),
    path('dashboard/negocios/registro/',
         views.business_add, name='business_add'),
    path('panel/', views.panel, name='panel'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/consultar', views.clientes_consultar, name='clientes_consultar'),
]
