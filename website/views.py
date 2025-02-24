from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record, Note
from django.db.models import Count
from django.db.models.functions import TruncMonth, ExtractMonth
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden


def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    notes = client.notes.all()  # Obtiene todas las notas relacionadas con este cliente
    return render(request, 'client_detail.html', {'client': client, 'notes': notes})

#Usuario

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
			return redirect('home')
		else:
			messages.success(request, "Hubo un error al ingresar, por favor intente de nuevo.")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})

#def login_user(request):

def logout_user(request):
	logout(request)
	messages.success(request, "Saliste.")
	return redirect('home')
    
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Te has registrado con exito.')
            return redirect('home')
    else:
        form = SignUpForm()
        return render (request, 'register.html', {'form':form})
    
    return render (request, 'register.html', {'form':form})
    
#CRUD
   
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Record

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Obtenemos el Record con el ID especificado
        customer_record = get_object_or_404(Record, id=pk)

        # Obtener las notas asociadas con el cliente desde el modelo Note
        notes = Note.objects.filter(client=customer_record)  # Notas relacionadas con el cliente

        return render(request, 'record.html', {
            'customer_record': customer_record,
            'notes': notes,  # Pasamos las notas a la plantilla
        })
    else:
        messages.success(request, 'Tienes que ingresar')
        return redirect('home')
     

def delete_record(request, pk):
    try:
        record = Record.objects.get(id=pk)
    except Record.DoesNotExist:
        messages.error(request, "Cliente no encontrado.")
        return redirect('records')  # Redirige a la vista de todos los registros si no se encuentra el registro
    # Verifica si el usuario tiene el permiso adecuado
    if not request.user.has_perm('website.delete_record'):
        messages.error(request, "No tienes los permisos para borrar clientes.")
        return redirect('record', pk=pk)  # Redirige a la vista de registros si no tiene permiso
    # Si el usuario tiene permiso, se elimina el registro
    record.delete()
    messages.success(request, "El cliente ha sido eliminado exitosamente!")
    return redirect('record', pk=pk)  # Redirige a la vista de todos los registros después de la eliminación

def add_record(request):
    # Verifica si el usuario tiene el permiso adecuado para agregar un registro
    if not request.user.has_perm('website.add_record'):
        messages.error(request, "No tienes los permisos para añadir clientes.")
        return redirect('home')  # Redirige al home si no tiene permiso
    if request.method == "POST":
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nuevo cliente añadido exitosamente!")
            return redirect('home')  # Redirige al home después de agregar el registro exitosamente
    else:
        form = AddRecordForm()
    return render(request, 'add_record.html', {'form': form})

def update_record(request, pk):
    try:
        record = Record.objects.get(id=pk)
    except Record.DoesNotExist:
        messages.error(request, "Cliente no encontrado.")
        return redirect('record', pk=pk)  # Donde `record_id` es el identificador del registro
    # Verifica si el usuario tiene el permiso adecuado
    if not request.user.has_perm('website.update_record'):
        messages.error(request, "No tienes los permisos para actualizar clientes.")
        return redirect('record', pk=pk)  # Donde `record_id` es el identificador del registro
        # Redirige a la vista record
    # Si el usuario tiene permiso, se permite editar
    if request.method == "POST":
        form = AddRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado exitosamente!")
            return redirect('home')  # Redirige después de una actualización exitosa
    else:
        form = AddRecordForm(instance=record)
    return render(request, 'update_record.html', {'form': form})
     
#Dashboard

def dashboard(request):
    # Si el usuario no está autenticado, redirigir a la página principal
    if not request.user.is_authenticated:
        # En lugar de redirigir a login, vamos a redirigir a home
        return redirect('home')
    
    # Obtener datos para los gráficos
    city_data = Record.objects.values('city').annotate(count=Count('id'))
    
    # Datos mensuales
    monthly_data = Record.objects.annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Preparar datos para las plantillas
    cities = [city['city'] for city in city_data]
    city_counts = [city['count'] for city in city_data]
    
    months = [str(data['month']) for data in monthly_data]
    monthly_counts = [data['count'] for data in monthly_data]
    
    context = {
        'cities': cities,
        'city_counts': city_counts,
        'months': months,
        'monthly_counts': monthly_counts,
    }
    
    return render(request, 'dashboard.html', context)