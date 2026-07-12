from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Requerido. Máximo 150 caracteres. Solo letras, dígitos y @/./+/-/_.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Tu contraseña no puede ser muy similar a tu información personal.</li><li>Debe contener al menos 8 caracteres.</li><li>No puede ser una contraseña de uso común.</li><li>No puede ser completamente numérica.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme contraseña'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Ingresa de nuevo la contraseña.</small></span>'


class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Primer Nombre", "class": "form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Apellido", "class": "form-control"}), label="")
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Fono", "class": "form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Dirección", "class": "form-control"}), label="")
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Ciudad", "class": "form-control"}), label="")

    class Meta:
        model = Record
        exclude = ("created_at",)
