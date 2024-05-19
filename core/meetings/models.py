from django.db import models
from core.employee.models import Worker, Field
from django.forms import model_to_dict
from django.urls import reverse
from django.utils import timezone

# Create your models here.

meeting_type_choices = (("G", "Generales"), ("A", "Área"), ("D", "Directivos"))


class Meeting(models.Model):
    name = models.CharField("Tema", max_length=50)
    organizer = models.ForeignKey(
        Worker, verbose_name="Organizador", on_delete=models.PROTECT
    )
    link = models.URLField("link", max_length=200)
    type = models.CharField(
        "Tipo de reunión", max_length=1, choices=meeting_type_choices
    )
    field = models.ForeignKey(
        Field,
        verbose_name="Área",
        on_delete=models.PROTECT,
        null=True,
        help_text="Seleccionar para reunión por área",
        blank=True,
    )
    date = models.DateTimeField("Fecha", auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "Reunion"
        verbose_name_plural = "Reuniones"

    def __str__(self):
        return self.name

    def toJson(self):
        return model_to_dict(self)

    def get_attendances_url(self):
        return reverse("attendances", kwargs={"pk": self.pk})

    def get_natural_date(self):
        return self.date.astimezone(timezone.get_default_timezone()).strftime(
            "el día %d de %B del %Y a las %I:%M %p"
        )


class Attendance(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        verbose_name="Reunion",
        on_delete=models.CASCADE,
        related_name="attendances",
    )
    worker = models.ForeignKey(
        Worker, verbose_name="Trabajador", on_delete=models.CASCADE
    )
    status = models.CharField(
        verbose_name="estado", max_length=1, null=True, blank=True
    )
    justification = models.CharField("justificacion", max_length=150)

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"

    def __str__(self):
        return f" A-{self.meeting}-{self.worker}"
