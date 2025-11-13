from django.contrib import admin
from .models import Autor, Editorial, Cliente, Libro, Venta, DetalleVenta

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['clienteid', 'nombre', 'apellido', 'email', 'telefono', 'fecharegistro']
    search_fields = ['nombre', 'apellido', 'email']
    list_filter = ['fecharegistro']

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['autorid', 'nombre', 'apellido', 'nacionalidad']
    search_fields = ['nombre', 'apellido']

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ['editorialid', 'nombreeditorial', 'emailcontacto', 'paisorigen']
    search_fields = ['nombreeditorial']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['libroid', 'titulo', 'autor', 'editorial', 'precioventa', 'stock']
    list_filter = ['genero', 'editorial']
    search_fields = ['titulo', 'isbn']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['ventaid', 'cliente', 'fechaventa', 'montototal', 'estadoVenta']
    list_filter = ['estadoVenta', 'fechaventa']

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['detalleDeLaVentaid', 'venta', 'libro', 'cantidad', 'subtotal']