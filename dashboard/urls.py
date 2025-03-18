from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="dashboard"),
    path('logout/', signout, name="logout"),
    path('usuarios/', users, name="users"),
    path('usuarios/crear/', users_manage, name="users_create"),
    path('usuarios/editar/<int:pk>/', users_manage, name="users_edit"),
    path('usuarios/borrar/<int:pk>/', users_manage, name="users_delete"),
    path('marcas/', brands, name="brands"),
    path('marcas/crear/', brands_manage, name="brands_create"),
    path('marcas/editar/<int:pk>/', brands_manage, name="brands_edit"),
    path('marcas/borrar/<int:pk>/', brands_manage, name="brands_delete"),
    path('departamentos/', departments, name="departments"),
    path('departamentos/crear/', departments_manage, name="departments_create"),
    path('departamentos/editar/<int:pk>/',
         departments_manage, name="departments_edit"),
    path('departamentos/borrar/<int:pk>/',
         departments_manage, name="departments_delete"),
    path('medidas/', sizes, name="sizes"),
    path('medidas/crear/', sizes_manage, name="sizes_create"),
    path('medidas/editar/<int:pk>/', sizes_manage, name="sizes_edit"),
    path('medidas/borrar/<int:pk>/', sizes_manage, name="sizes_delete"),
]
