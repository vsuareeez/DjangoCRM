from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User

# Create your models here.
class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    email =  models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address =  models.CharField(max_length=100)
    city =  models.CharField(max_length=50)
    image = models.ImageField(upload_to='customer_images/', blank=True, null=True)
 
    history = HistoricalRecords()
    
    def __str__(self):
        return(f"{self.first_name} {self.last_name}")
    
class Note(models.Model):
    client = models.ForeignKey('Record', on_delete=models.CASCADE, related_name='notes')  # Relacionada con el cliente
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Quién escribió la nota
    content = models.TextField()  # Contenido de la nota
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización

    def __str__(self):
        return f"Nota para {self.client} por {self.author}"