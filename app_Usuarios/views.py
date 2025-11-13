from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def inicio_publico(request):
    """Vista pública que muestra información de la librería"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'inicio_publico.html')

def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('inicio_sesion')
    
    # Si ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'usuarios/inicio_sesion.html')

@login_required
def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('inicio_publico')  # Cambiar a la vista pública

@login_required
def perfil_usuario(request):
    return render(request, 'usuarios/perfil.html')