from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control text-white',
        'placeholder': 'Email',
        'style': 'color: white !important;'
    }))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control text-white',
        'placeholder': 'Nombre',
        'style': 'color: white !important;'
    }))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control text-white',
        'placeholder': 'Apellido',
        'style': 'color: white !important;'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Estilo para el campo de usuario
        self.fields['username'].widget.attrs.update({
            'class': 'form-control text-white',
            'placeholder': 'Usuario',
            'style': 'color: white !important;'
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text" style="color: white !important;"><small>Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ únicamente.</small></span>'

        # Estilo para la contraseña 1
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control text-white',
            'placeholder': 'Contraseña',
            'style': 'color: white !important;'
        })
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '''
        <ul class="form-text" style="color: white !important; list-style: disc; padding-left: 20px;">
            <li>Tu contraseña no puede ser similar a tu información personal</li>
            <li>Debe contener al menos 8 caracteres</li>
            <li>No puede ser una contraseña comúnmente usada</li>
            <li>No puede ser completamente numérica</li>
        </ul>
        '''

        # Estilo para la contraseña 2
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control text-white',
            'placeholder': 'Confirme contraseña',
            'style': 'color: white !important;'
        })
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text" style="color: white !important;"><small>Ingresa de nuevo la contraseña.</small></span>'


class AddRecordForm(forms.ModelForm):
    # Campos con estilo para texto blanco
    field_style = 'color: black !important;'
    field_class = 'form-control text-white'
    
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "placeholder": "Nombre",
        "class": field_class,
        "style": field_style
    }), label="")
    
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "placeholder": "Apellido",
        "class": field_class,
        "style": field_style
    }), label="")
    
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "placeholder": "Email",
        "class": field_class,
        "style": field_style
    }), label="")
    
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "placeholder": "Fono",
        "class": field_class,
        "style": field_style
    }), label="")
    
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "placeholder": "Dirección",
        "class": field_class,
        "style": field_style
    }), label="")
    
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "placeholder": "Ciudad",
        "class": field_class,
        "style": field_style
    }), label="")

    class Meta:
        model = Record
        exclude = ("user",)