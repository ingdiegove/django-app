"""crud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tareas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registro', views.registro, name='registro'),
    path('tareas', views.tareas, name='tareas'),
    path('tareas_completadas', views.tareas_completadas, name='tareas_completadas'),
    path('tareas/crear_tareas/', views.crear_tareas, name='crear_tareas'),
    path('tareas/<int:tareas_id>', views.tareas_detalles, name='tareas_detalles'),
    path('tareas/<int:tareas_id>/completar', views.completar_tareas, name='completar_tareas'),
    path('tareas/<int:tareas_id>/eliminar', views.eliminar_tareas, name='eliminar_tareas'),
    path('cerrarsesion', views.cerrarsesion, name='cerrarsesion'),
    path('iniciarsesion', views.iniciarsesion, name='iniciarsesion')
]
