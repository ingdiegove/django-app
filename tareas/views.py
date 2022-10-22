
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #libreria para formulario de registro
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponse
from .forms import TareasFormulario
from .models import Tareas
from django.utils import timezone
from django.contrib.auth.decorators import login_required 
# Create your views here.

def home(request):
    return render(request, 'home.html')

def registro(request):

    if request.method == 'GET':
        return render(request, 'registro.html', {
            'formulario': UserCreationForm
    })

    else:
        if request.POST['password1'] == request.POST['password2']:
           #registro usuario
            try:
                user = User.objects.create_user(username=request.POST   ['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tareas')
            except: IntegrityError

            return render(request, 'registro.html', {
                "formulario": UserCreationForm,
                "error": "Usuario ya Existe."})
    
        return render(request, 'registro.html', {
            "formulario": UserCreationForm, 
            "error": "La clave no coinside" })

@login_required
def tareas(request):
    tarea = Tareas.objects.filter(user=request.user, fechacompletada__isnull=True)
    return render(request, 'tareas.html', {'tareas': tarea} )

@login_required
def tareas_completadas(request):
    tareas = Tareas.objects.filter(user=request.user, fechacompletada__isnull=False).order_by
    ('fechacompletada')
    return render(request, 'tareas.html', {'tareas': tareas} )    

@login_required
def crear_tareas(request):
    if request.method == 'GET':
        return render(request, 'crear_tareas.html', {
            'formulario': TareasFormulario
        })
    else:
        try:
            form = TareasFormulario(request.POST)
            nueva_tarea = form.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'crear_tareas.html', {
                "formulario": TareasFormulario,
                "error": "Por favor Ingrese datos validos."
            })   

@login_required
def tareas_detalles(request, tareas_id):
    if request.method == 'GET':
        tarea = get_object_or_404(Tareas, pk=tareas_id, user = request.user)
        formulario = TareasFormulario(instance=tarea)
        return render(request, 'tareas_detalles.html', {'tareas': tarea, 'formulario': formulario})
    else:
        try:
             tarea = get_object_or_404(Tareas, pk=tareas_id, user = request.user)
             formulario = TareasFormulario(request.POST, instance=tarea)
             formulario.save()
             return redirect('tareas')
        except: ValueError
        return render(request, 'tareas_detalles.html', {'tareas': tarea, 'formulario': formulario, 'error': 'Error al Actualizar la Tarea'})

@login_required
def completar_tareas(request, tareas_id):
    tarea = get_object_or_404(Tareas, pk=tareas_id, user = request.user)
    if request.method == 'POST':
        tarea.fechacompletada = timezone.now()
        tarea.save()
        return redirect('tareas')
@login_required
def eliminar_tareas(request, tareas_id):
    tarea = get_object_or_404(Tareas, pk=tareas_id, user = request.user)
    if request.method == 'POST':
        
        tarea.delete()
        return redirect('tareas')      
@login_required
def cerrarsesion(request):
     logout(request)
     return redirect('home')   

def iniciarsesion(request):
    if request.method == 'GET':
        return render(request, 'iniciarsesion.html', {"formulario": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'iniciarsesion.html', {
                "formulario": AuthenticationForm, 
                "error": "Usuario o Contraseña son Incorrecto."})

        else:
            login(request, user)
            return redirect('tareas')

   