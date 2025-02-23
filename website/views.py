from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.db.models import Count
from django.db.models.functions import TruncMonth, ExtractMonth
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden




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
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})


#def login_user(request):


def logout_user(request):
	logout(request)
	messages.success(request, "You logged out")
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
            messages.success(request, 'You have registered')
            return redirect('home')
    else:
        form = SignUpForm()
        return render (request, 'register.html', {'form':form})
    
    return render (request, 'register.html', {'form':form})
    
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render (request, 'record.html', {'customer_record':customer_record})
    else: 
        messages.success(request, 'You must be logged in')
        return redirect('home')
        

def delete_record(request, pk):
    try:
        record = Record.objects.get(id=pk)
    except Record.DoesNotExist:
        messages.error(request, "Record not found.")
        return redirect('records')  # Redirige a la vista de todos los registros si no se encuentra el registro
    # Verifica si el usuario tiene el permiso adecuado
    if not request.user.has_perm('website.delete_record'):
        messages.error(request, "You do not have permission to delete this record.")
        return redirect('record', pk=pk)  # Redirige a la vista de registros si no tiene permiso
    # Si el usuario tiene permiso, se elimina el registro
    record.delete()
    messages.success(request, "Record has been deleted successfully!")
    return redirect('record', pk=pk)  # Redirige a la vista de todos los registros después de la eliminación

def add_record(request):
    # Verifica si el usuario tiene el permiso adecuado para agregar un registro
    if not request.user.has_perm('website.add_record'):
        messages.error(request, "You do not have permission to add a record.")
        return redirect('home')  # Redirige al home si no tiene permiso
    if request.method == "POST":
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New record has been added successfully!")
            return redirect('home')  # Redirige al home después de agregar el registro exitosamente
    else:
        form = AddRecordForm()
    return render(request, 'add_record.html', {'form': form})

def update_record(request, pk):
    try:
        record = Record.objects.get(id=pk)
    except Record.DoesNotExist:
        messages.error(request, "Record not found.")
        return redirect('record', pk=pk)  # Donde `record_id` es el identificador del registro
    # Verifica si el usuario tiene el permiso adecuado
    if not request.user.has_perm('website.update_record'):
        messages.error(request, "You do not have permission to update this record.")
        return redirect('record', pk=pk)  # Donde `record_id` es el identificador del registro
        # Redirige a la vista record
    # Si el usuario tiene permiso, se permite editar
    if request.method == "POST":
        form = AddRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated successfully!")
            return redirect('home')  # Redirige después de una actualización exitosa
    else:
        form = AddRecordForm(instance=record)
    return render(request, 'update_record.html', {'form': form})
     

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