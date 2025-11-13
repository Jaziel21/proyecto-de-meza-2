from django.urls import path
from . import views

urlpatterns = [
    # ========== URLs PÚBLICAS (SOLO LECTURA) ==========
    path('public/autores/', views.public_autores, name='public_autores'),
    path('public/editoriales/', views.public_editoriales, name='public_editoriales'),
    path('public/clientes/', views.public_clientes, name='public_clientes'),
    path('public/libros/', views.public_libros, name='public_libros'),
    path('public/ventas/', views.public_ventas, name='public_ventas'),
    
    # ========== URLs PRIVADAS (CRUD COMPLETO) ==========
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Autores
    path('autores/', views.lista_autores, name='lista_autores'),
    path('autores/agregar/', views.agregar_autor, name='agregar_autor'),
    path('autores/editar/<int:autor_id>/', views.editar_autor, name='editar_autor'),
    path('autores/eliminar/<int:autor_id>/', views.eliminar_autor, name='eliminar_autor'),
    
    # Editoriales
    path('editoriales/', views.lista_editoriales, name='lista_editoriales'),
    path('editoriales/agregar/', views.agregar_editorial, name='agregar_editorial'),
    path('editoriales/editar/<int:editorial_id>/', views.editar_editorial, name='editar_editorial'),
    path('editoriales/eliminar/<int:editorial_id>/', views.eliminar_editorial, name='eliminar_editorial'),
    
    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # Libros
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/agregar/', views.agregar_libro, name='agregar_libro'),
    path('libros/editar/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('libros/eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    
    # Ventas
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    path('ventas/editar/<int:venta_id>/', views.editar_venta, name='editar_venta'),
    path('ventas/eliminar/<int:venta_id>/', views.eliminar_venta, name='eliminar_venta'),
    path('ventas/detalle/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    
    # Detalles de Venta
    path('detalles/agregar/', views.agregar_detalle_venta, name='agregar_detalle_venta'),
    path('detalles/eliminar/<int:detalle_id>/', views.eliminar_detalle_venta, name='eliminar_detalle_venta'),
]