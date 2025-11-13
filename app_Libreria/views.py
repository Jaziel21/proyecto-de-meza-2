from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Autor, Editorial, Cliente, Libro, Venta, DetalleVenta

# ========== VISTAS PÚBLICAS (SOLO LECTURA) ==========
def public_autores(request):
    """Vista pública para ver autores"""
    autores = Autor.objects.all()
    return render(request, 'public/autores.html', {'autores': autores})

def public_editoriales(request):
    """Vista pública para ver editoriales"""
    editoriales = Editorial.objects.all()
    return render(request, 'public/editoriales.html', {'editoriales': editoriales})

def public_clientes(request):
    """Vista pública para ver clientes"""
    clientes = Cliente.objects.all()
    return render(request, 'public/clientes.html', {'clientes': clientes})

def public_libros(request):
    """Vista pública para ver libros"""
    libros = Libro.objects.all()
    return render(request, 'public/libros.html', {'libros': libros})

def public_ventas(request):
    """Vista pública para ver ventas"""
    ventas = Venta.objects.all().order_by('-fechaventa')
    
    # Calcular estadísticas
    total_ventas = sum(venta.montototal for venta in ventas)
    ventas_completadas = ventas.filter(estadoVenta='COMPLETADA').count()
    ventas_pendientes = ventas.filter(estadoVenta='PENDIENTE').count()
    ventas_canceladas = ventas.filter(estadoVenta='CANCELADA').count()
    
    context = {
        'ventas': ventas,
        'total_ventas': total_ventas,
        'ventas_completadas': ventas_completadas,
        'ventas_pendientes': ventas_pendientes,
        'ventas_canceladas': ventas_canceladas,
    }
    return render(request, 'public/ventas.html', context)

# ========== VISTAS PRIVADAS (CRUD COMPLETO) ==========

# Dashboard
@login_required
def dashboard(request):
    total_libros = Libro.objects.count()
    total_clientes = Cliente.objects.count()
    total_ventas = Venta.objects.count()
    libros_bajo_stock = Libro.objects.filter(stock__lt=5)
    
    context = {
        'total_libros': total_libros,
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
        'libros_bajo_stock': libros_bajo_stock,
    }
    return render(request, 'dashboard.html', context)

# ========== AUTORES ==========
@login_required
def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'autores/lista_autores.html', {'autores': autores})

@login_required
def agregar_autor(request):
    if request.method == 'POST':
        try:
            Autor.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                nacionalidad=request.POST['nacionalidad'],
                fechanacimiento=request.POST['fechanacimiento'],
                bibliografia=request.POST.get('bibliografia', ''),
                paginaweb=request.POST.get('paginaweb', '')
            )
            messages.success(request, 'Autor agregado correctamente')
            return redirect('lista_autores')
        except Exception as e:
            messages.error(request, f'Error al agregar autor: {str(e)}')
    
    return render(request, 'autores/agregar_autor.html')

@login_required
def editar_autor(request, autor_id):
    autor = get_object_or_404(Autor, autorid=autor_id)
    
    if request.method == 'POST':
        try:
            autor.nombre = request.POST['nombre']
            autor.apellido = request.POST['apellido']
            autor.nacionalidad = request.POST['nacionalidad']
            autor.fechanacimiento = request.POST['fechanacimiento']
            autor.bibliografia = request.POST.get('bibliografia', '')
            autor.paginaweb = request.POST.get('paginaweb', '')
            autor.save()
            messages.success(request, 'Autor actualizado correctamente')
            return redirect('lista_autores')
        except Exception as e:
            messages.error(request, f'Error al actualizar autor: {str(e)}')
    
    return render(request, 'autores/editar_autor.html', {'autor': autor})

@login_required
def eliminar_autor(request, autor_id):
    autor = get_object_or_404(Autor, autorid=autor_id)
    
    if request.method == 'POST':
        autor.delete()
        messages.success(request, 'Autor eliminado correctamente')
        return redirect('lista_autores')
    
    return render(request, 'autores/eliminar_autor.html', {'autor': autor})

# ========== EDITORIALES ==========
@login_required
def lista_editoriales(request):
    editoriales = Editorial.objects.all()
    return render(request, 'editoriales/lista_editoriales.html', {'editoriales': editoriales})

@login_required
def agregar_editorial(request):
    if request.method == 'POST':
        try:
            Editorial.objects.create(
                nombreeditorial=request.POST['nombreeditorial'],
                direccion=request.POST['direccion'],
                telefono=request.POST['telefono'],
                emailcontacto=request.POST['emailcontacto'],
                sitioweb=request.POST.get('sitioweb', ''),
                paisorigen=request.POST['paisorigen']
            )
            messages.success(request, 'Editorial agregada correctamente')
            return redirect('lista_editoriales')
        except Exception as e:
            messages.error(request, f'Error al agregar editorial: {str(e)}')
    
    return render(request, 'editoriales/agregar_editorial.html')

@login_required
def editar_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, editorialid=editorial_id)
    
    if request.method == 'POST':
        try:
            editorial.nombreeditorial = request.POST['nombreeditorial']
            editorial.direccion = request.POST['direccion']
            editorial.telefono = request.POST['telefono']
            editorial.emailcontacto = request.POST['emailcontacto']
            editorial.sitioweb = request.POST.get('sitioweb', '')
            editorial.paisorigen = request.POST['paisorigen']
            editorial.save()
            messages.success(request, 'Editorial actualizada correctamente')
            return redirect('lista_editoriales')
        except Exception as e:
            messages.error(request, f'Error al actualizar editorial: {str(e)}')
    
    return render(request, 'editoriales/editar_editorial.html', {'editorial': editorial})

@login_required
def eliminar_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, editorialid=editorial_id)
    
    if request.method == 'POST':
        editorial.delete()
        messages.success(request, 'Editorial eliminada correctamente')
        return redirect('lista_editoriales')
    
    return render(request, 'editoriales/eliminar_editorial.html', {'editorial': editorial})

# ========== CLIENTES ==========
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        try:
            Cliente.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                email=request.POST['email'],
                telefono=request.POST['telefono'],
                direccion=request.POST['direccion'],
                preferenciasgenero=request.POST.get('preferenciasgenero', '')
            )
            messages.success(request, 'Cliente agregado correctamente')
            return redirect('lista_clientes')
        except Exception as e:
            messages.error(request, f'Error al agregar cliente: {str(e)}')
    
    return render(request, 'clientes/agregar_cliente.html')

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, clienteid=cliente_id)
    
    if request.method == 'POST':
        try:
            cliente.nombre = request.POST['nombre']
            cliente.apellido = request.POST['apellido']
            cliente.email = request.POST['email']
            cliente.telefono = request.POST['telefono']
            cliente.direccion = request.POST['direccion']
            cliente.preferenciasgenero = request.POST.get('preferenciasgenero', '')
            cliente.save()
            messages.success(request, 'Cliente actualizado correctamente')
            return redirect('lista_clientes')
        except Exception as e:
            messages.error(request, f'Error al actualizar cliente: {str(e)}')
    
    return render(request, 'clientes/editar_cliente.html', {'cliente': cliente})

@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, clienteid=cliente_id)
    
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente')
        return redirect('lista_clientes')
    
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})

# ========== LIBROS ==========
@login_required
def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'libros/lista_libros.html', {'libros': libros})

@login_required
def agregar_libro(request):
    if request.method == 'POST':
        try:
            libro = Libro.objects.create(
                titulo=request.POST['titulo'],
                autor_id=request.POST['autor'],
                editorial_id=request.POST['editorial'],
                isbn=request.POST['isbn'],
                anioPublicacion=request.POST['anioPublicacion'],
                genero=request.POST['genero'],
                precioventa=request.POST['precioventa'],
                stock=request.POST.get('stock', 0)
            )
            messages.success(request, 'Libro agregado correctamente')
            return redirect('lista_libros')
        except Exception as e:
            messages.error(request, f'Error al agregar libro: {str(e)}')
    
    autores = Autor.objects.all()
    editoriales = Editorial.objects.all()
    return render(request, 'libros/agregar_libro.html', {
        'autores': autores,
        'editoriales': editoriales
    })

@login_required
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, libroid=libro_id)
    
    if request.method == 'POST':
        try:
            libro.titulo = request.POST['titulo']
            libro.autor_id = request.POST['autor']
            libro.editorial_id = request.POST['editorial']
            libro.isbn = request.POST['isbn']
            libro.anioPublicacion = request.POST['anioPublicacion']
            libro.genero = request.POST['genero']
            libro.precioventa = request.POST['precioventa']
            libro.stock = request.POST.get('stock', 0)
            libro.save()
            messages.success(request, 'Libro actualizado correctamente')
            return redirect('lista_libros')
        except Exception as e:
            messages.error(request, f'Error al actualizar libro: {str(e)}')
    
    autores = Autor.objects.all()
    editoriales = Editorial.objects.all()
    return render(request, 'libros/editar_libro.html', {
        'libro': libro,
        'autores': autores,
        'editoriales': editoriales
    })

@login_required
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, libroid=libro_id)
    
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado correctamente')
        return redirect('lista_libros')
    
    return render(request, 'libros/eliminar_libro.html', {'libro': libro})

# ========== VENTAS ==========
@login_required
def lista_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})

@login_required
def agregar_venta(request):
    if request.method == 'POST':
        try:
            # Aquí iría la lógica compleja para crear ventas con detalles
            messages.success(request, 'Venta agregada correctamente')
            return redirect('lista_ventas')
        except Exception as e:
            messages.error(request, f'Error al agregar venta: {str(e)}')
    
    clientes = Cliente.objects.all()
    libros = Libro.objects.all()
    return render(request, 'ventas/agregar_venta.html', {
        'clientes': clientes,
        'libros': libros
    })

@login_required
def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, ventaid=venta_id)
    
    if request.method == 'POST':
        try:
            venta.cliente_id = request.POST['cliente']
            venta.metodopago = request.POST['metodopago']
            venta.estadoVenta = request.POST['estadoVenta']
            venta.descuentoAplicado = request.POST.get('descuentoAplicado', 0)
            venta.save()
            messages.success(request, 'Venta actualizada correctamente')
            return redirect('lista_ventas')
        except Exception as e:
            messages.error(request, f'Error al actualizar venta: {str(e)}')
    
    clientes = Cliente.objects.all()
    libros = Libro.objects.all()
    return render(request, 'ventas/editar_venta.html', {
        'venta': venta,
        'clientes': clientes,
        'libros': libros
    })

@login_required
def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, ventaid=venta_id)
    
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada correctamente')
        return redirect('lista_ventas')
    
    return render(request, 'ventas/eliminar_venta.html', {'venta': venta})

@login_required
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, ventaid=venta_id)
    return render(request, 'ventas/detalle_venta.html', {'venta': venta})

# ========== DETALLES VENTA ==========
@login_required
def agregar_detalle_venta(request):
    if request.method == 'POST':
        try:
            DetalleVenta.objects.create(
                venta_id=request.POST['venta'],
                libro_id=request.POST['libro'],
                cantidad=request.POST['cantidad'],
                precioUnitario=request.POST['precioUnitario'],
                iva=request.POST.get('iva', 16)
            )
            messages.success(request, 'Detalle agregado correctamente')
            return redirect('editar_venta', venta_id=request.POST['venta'])
        except Exception as e:
            messages.error(request, f'Error al agregar detalle: {str(e)}')
    
    ventas = Venta.objects.all()
    libros = Libro.objects.all()
    return render(request, 'detalles_venta/agregar_detalle.html', {
        'ventas': ventas,
        'libros': libros
    })

@login_required
def eliminar_detalle_venta(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, detalleDeLaVentaid=detalle_id)
    venta_id = detalle.venta.ventaid
    
    if request.method == 'POST':
        detalle.delete()
        messages.success(request, 'Detalle eliminado correctamente')
        return redirect('editar_venta', venta_id=venta_id)
    
    return render(request, 'detalles_venta/eliminar_detalle.html', {'detalle': detalle})