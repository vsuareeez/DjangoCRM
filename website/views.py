from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.views.decorators.http import require_POST

from .forms import SignUpForm, AddRecordForm
from .models import Record


# Usuario

def home(request):
    records = Record.objects.all()
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Has ingresado!")
        else:
            messages.error(request, "Hubo un error al ingresar, por favor intente de nuevo.")
        return redirect('home')
    return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "Saliste.")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Te has registrado con exito.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


# CRUD

@login_required
def customer_record(request, pk):
    # Obtenemos el Record con el ID especificado
    customer_record = get_object_or_404(Record, id=pk)

    # Notas relacionadas con el cliente (related_name='notes' en el modelo Note)
    notes = customer_record.notes.all()

    return render(request, 'record.html', {
        'customer_record': customer_record,
        'notes': notes,
    })


@login_required
@require_POST
def delete_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    if not request.user.has_perm('website.delete_record'):
        messages.error(request, "No tienes los permisos para borrar clientes.")
        return redirect('record', pk=pk)
    record.delete()
    messages.success(request, "El cliente ha sido eliminado exitosamente!")
    return redirect('home')


@login_required
def add_record(request):
    if not request.user.has_perm('website.add_record'):
        messages.error(request, "No tienes los permisos para añadir clientes.")
        return redirect('home')
    if request.method == "POST":
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nuevo cliente añadido exitosamente!")
            return redirect('home')
    else:
        form = AddRecordForm()
    return render(request, 'add_record.html', {'form': form})


@login_required
def update_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    if not request.user.has_perm('website.change_record'):
        messages.error(request, "No tienes los permisos para actualizar clientes.")
        return redirect('record', pk=pk)
    if request.method == "POST":
        form = AddRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado exitosamente!")
            return redirect('home')
    else:
        form = AddRecordForm(instance=record)
    return render(request, 'update_record.html', {'form': form})


# Dashboard

@login_required
def dashboard(request):
    # Datos para el gráfico por ciudad
    city_data = Record.objects.values('city').annotate(count=Count('id'))

    # Datos mensuales
    monthly_data = Record.objects.annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    context = {
        'cities': [city['city'] for city in city_data],
        'city_counts': [city['count'] for city in city_data],
        'months': [str(data['month']) for data in monthly_data],
        'monthly_counts': [data['count'] for data in monthly_data],
    }

    return render(request, 'dashboard.html', context)
