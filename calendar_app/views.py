# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from django.utils import timezone
from django.http import JsonResponse
import json
from django.utils.dateformat import DateFormat

def event_calendar(request):
    events = Event.objects.all()
    events_list = [{'title': event.title, 'start': event.date.strftime('%Y-%m-%d')} for event in events]
    events_json = json.dumps(events_list)  # Convierte la lista a JSON
    return render(request, 'calendar.html', {'events': events_json})


def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        Event.objects.create(title=title, description=description, date=date)
        return redirect('calendar')
    return render(request, 'add_event.html')
