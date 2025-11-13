from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_publico, name='inicio_publico'),  # Página pública principal
    path('login/', views.inicio_sesion, name='inicio_sesion'),  # Formulario de login
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
]