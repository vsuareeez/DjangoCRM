from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import EventForm
from .models import Event


@login_required
def event_calendar(request):
    events = Event.objects.all()
    events_list = [{'title': event.title, 'start': event.date.strftime('%Y-%m-%d')} for event in events]

    hoy = date.today()
    events_this_month = Event.objects.filter(date__year=hoy.year, date__month=hoy.month).count()

    return render(request, 'calendar.html', {
        'events': events_list,
        'events_this_month': events_this_month,
        'has_events': events.exists(),
    })


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento agregado exitosamente!")
            return redirect('calendar')
    else:
        form = EventForm(initial={'date': request.GET.get('date')})
    return render(request, 'add_event.html', {'form': form})
