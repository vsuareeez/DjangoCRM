from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from django.views.decorators.http import require_POST

from calendar_app.models import Event
from .forms import SignUpForm, AddRecordForm
from .models import Record

MESES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']


def _inicio_de_mes(momento):
    return momento.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


# Usuario

def home(request):
    # Página de login; los usuarios autenticados van directo a la lista de clientes
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Has ingresado!")
            return redirect('clientes')
        messages.error(request, "Usuario o contraseña incorrectos, intenta de nuevo.")
        return redirect('home')
    if request.user.is_authenticated:
        return redirect('clientes')
    return render(request, 'home.html')


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
            return redirect('clientes')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


# CRUD

@login_required
def clientes(request):
    records = Record.objects.order_by('-created_at')
    total_count = records.count()
    new_this_month = records.filter(created_at__gte=_inicio_de_mes(timezone.now())).count()
    cities = (Record.objects.exclude(city='').order_by('city')
              .values_list('city', flat=True).distinct())

    paginator = Paginator(records, 8)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'clientes.html', {
        'page_obj': page_obj,
        'total_count': total_count,
        'new_this_month': new_this_month,
        'cities': cities,
    })


@login_required
def customer_record(request, pk):
    customer_record = get_object_or_404(Record, id=pk)
    notes = customer_record.notes.select_related('author').order_by('-created_at')
    return render(request, 'record.html', {
        'customer_record': customer_record,
        'notes': notes,
    })


@login_required
@require_POST
def add_note(request, pk):
    record = get_object_or_404(Record, id=pk)
    content = request.POST.get('content', '').strip()
    if content:
        record.notes.create(author=request.user, content=content)
        messages.success(request, "Nota guardada.")
    else:
        messages.error(request, "La nota no puede estar vacía.")
    return redirect('record', pk=pk)


@login_required
@require_POST
def delete_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    if not request.user.has_perm('website.delete_record'):
        messages.error(request, "No tienes los permisos para borrar clientes.")
        return redirect('record', pk=pk)
    record.delete()
    messages.success(request, "El cliente ha sido eliminado exitosamente!")
    return redirect('clientes')


@login_required
def add_record(request):
    if not request.user.has_perm('website.add_record'):
        messages.error(request, "No tienes los permisos para añadir clientes.")
        return redirect('clientes')
    if request.method == "POST":
        form = AddRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save()
            messages.success(request, "Cliente añadido correctamente.")
            return redirect('record', pk=record.pk)
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
        form = AddRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado exitosamente!")
            return redirect('record', pk=pk)
    else:
        form = AddRecordForm(instance=record)
    return render(request, 'update_record.html', {'form': form})


# Dashboard

@login_required
def dashboard(request):
    ahora = timezone.now()
    inicio_mes = _inicio_de_mes(ahora)

    total_count = Record.objects.count()
    new_this_month = Record.objects.filter(created_at__gte=inicio_mes).count()

    # Mes anterior (para el texto "vs. N en <mes>")
    prev_year, prev_month = (ahora.year, ahora.month - 1) if ahora.month > 1 else (ahora.year - 1, 12)
    inicio_mes_anterior = inicio_mes.replace(year=prev_year, month=prev_month)
    prev_month_count = Record.objects.filter(
        created_at__gte=inicio_mes_anterior, created_at__lt=inicio_mes
    ).count()

    # Clientes por ciudad (para la dona y el KPI)
    city_data = (Record.objects.exclude(city='').values('city')
                 .annotate(count=Count('id')).order_by('-count'))
    cities_count = len(city_data)
    top_city = city_data[0] if city_data else None

    # Registros de los últimos 6 meses (para las barras)
    monthly_labels, monthly_counts = [], []
    year, month = ahora.year, ahora.month
    meses_rango = []
    for _ in range(6):
        meses_rango.append((year, month))
        year, month = (year, month - 1) if month > 1 else (year - 1, 12)
    for y, m in reversed(meses_rango):
        siguiente = (y, m + 1) if m < 12 else (y + 1, 1)
        count = Record.objects.filter(
            created_at__gte=inicio_mes.replace(year=y, month=m),
            created_at__lt=inicio_mes.replace(year=siguiente[0], month=siguiente[1]),
        ).count()
        monthly_labels.append(MESES[m - 1])
        monthly_counts.append(count)

    upcoming_events = Event.objects.filter(date__gte=date.today()).count()

    return render(request, 'dashboard.html', {
        'total_count': total_count,
        'new_this_month': new_this_month,
        'prev_month_count': prev_month_count,
        'prev_month_name': MESES[prev_month - 1].lower(),
        'cities_count': cities_count,
        'top_city': top_city,
        'upcoming_events': upcoming_events,
        'cities_labels': [c['city'] for c in city_data],
        'cities_counts': [c['count'] for c in city_data],
        'monthly_labels': monthly_labels,
        'monthly_counts': monthly_counts,
    })
