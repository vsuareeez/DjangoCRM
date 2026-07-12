from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Reunión con María González"}),
        label="Título del Evento",
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Detalles del evento…"}),
        label="Descripción",
    )
    date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={"class": "form-control", "id": "date", "type": "date"}),
        label="Fecha",
        error_messages={'invalid': 'Ingresa una fecha válida (AAAA-MM-DD).'},
    )

    class Meta:
        model = Event
        fields = ('title', 'description', 'date')
