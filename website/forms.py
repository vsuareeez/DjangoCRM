from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record


class SignUpForm(UserCreationForm):
    # Los labels y textos de ayuda viven en register.html (rediseño DCRM)
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'camila@ejemplo.cl', 'autocomplete': 'email'}))
    first_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Camila', 'autocomplete': 'given-name'}))
    last_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Araya', 'autocomplete': 'family-name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'camila.a', 'autocomplete': 'username'})
        self.fields['username'].help_text = ''
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••', 'autocomplete': 'new-password'})
        self.fields['password1'].help_text = ''
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••', 'autocomplete': 'new-password'})
        self.fields['password2'].help_text = ''


class AddRecordForm(forms.ModelForm):
    # Solo nombre y apellido son obligatorios (regla del rediseño)
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "María", "class": "form-control"}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "González", "class": "form-control"}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"placeholder": "maria@ejemplo.cl", "class": "form-control"}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "+56 9 1234 5678", "class": "form-control", "type": "tel"}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Calle, número, depto", "class": "form-control"}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Santiago", "class": "form-control"}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={"class": "form-control"}))

    class Meta:
        model = Record
        exclude = ("created_at",)
