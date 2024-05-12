from django.db import models
from django.forms import model_to_dict
from django.urls import reverse
# Create your models here.

status_choices = (
    (1,'Activo'),
    (0,'Inactivo')
)


class Field(models.Model):
    name = models.CharField("Nombre", max_length=50)
    status = models.BooleanField("estado", default=True, choices=status_choices)

    def __str__(self):
        return self.name
    
    def toJson(self):
        return model_to_dict(self)
    
    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "areas"


class Position(models.Model):
    name = models.CharField("Nombre", max_length=50)
    status = models.BooleanField("estado", default=True, choices=status_choices)

    def __str__(self):
        return self.name

    def toJson(self):
        return model_to_dict(self)
    
    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
    

class Worker(models.Model):
    name = models.CharField("Nombre", max_length=30)
    last_name = models.CharField("Apellidos", max_length=70)
    birth_date = models.DateField("Fecha Nacimiento", auto_now=False, auto_now_add=False)
    address = models.CharField("Dirección", max_length=50)
    phone_number = models.CharField("Número de Télefono", max_length=50, help_text="Ejm : +51 963852741")
    field = models.ForeignKey(Field, verbose_name= "Área", on_delete=models.PROTECT)
    position = models.ForeignKey(Position, verbose_name="Cargo", on_delete=models.PROTECT)
    email = models.EmailField("Correo electronico", max_length=254)
    status = models.BooleanField("estado", default=True, choices=status_choices)

    def __str__(self):
        return self.name

    def toJson(self):
        return model_to_dict(self)
    
    def get_absolute_url(self):
        return reverse("worker_detail", kwargs={"pk": self.pk})
    
    def get_fullname(self):
        return f"{self.name} {self.last_name}"
    
    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"

