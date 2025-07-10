from django.db import models
from django.contrib.auth.models import User


class ResponsableObra(models.Model):
    nombre = models.CharField(max_length=100, unique=True , null=True)
    cip_cap = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.nombre} – CIP: {self.cip_cap}"

    class Meta:
        verbose_name = "Responsable de Obra"
        verbose_name_plural = "Responsables de Obra"

class SupervisorObra(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    cip_cap = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} – CIP: {self.cip_cap}"

    class Meta:
        verbose_name = "Supervisor de Obra"
        verbose_name_plural = "Supervisores de Obra"


class Zonificacion(models.Model):
    zonificacion = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=100, blank=True)
    departamento = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)

    def __str__(self):
        return self.zonificacion

    class Meta:
        verbose_name = "Zonificación"
        verbose_name_plural = "Zonificaciones"


class LicenciaUso(models.Model):
    nombre_licencia = models.CharField(max_length=100)
    uso_licencia = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_licencia

    class Meta:
        verbose_name = "Licencia de Uso"
        verbose_name_plural = "Licencias de Uso"


class Resolucion(models.Model):
    num_resolucion = models.CharField("N° Resolución", max_length=50, unique=True)
    num_expediente = models.CharField("N° Expediente", max_length=50, unique=True)
    num_recibo = models.CharField("N° Recibo", max_length=50, blank=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    administrado = models.CharField(max_length=100)
    propietario = models.BooleanField(default=True)
    nombre_licencia = models.ForeignKey(LicenciaUso, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=300, blank=True, default='')
    calle = models.CharField(max_length=200, blank=True, default='')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resoluciones')

    def __str__(self):
        return f"Num resolucion:{self.num_resolucion} / Num expediente:{self.num_expediente}"

    class Meta:
        verbose_name = "Resolución"
        verbose_name_plural = "Resoluciones"
        ordering = ['-fecha_emision']


class DetalleResolucion(models.Model):
    resolucion = models.OneToOneField(Resolucion, on_delete=models.CASCADE, null=True)
    zonificacion = models.ForeignKey(Zonificacion, on_delete=models.CASCADE)
    areatechada_total = models.DecimalField(max_digits=8, decimal_places=2)
    detalle_areatechada = models.TextField(blank=True, default='-')
    num_pisos = models.IntegerField()
    altura = models.DecimalField(max_digits=5, decimal_places=2, default='') 
    num_sotano = models.IntegerField(default=0)
    semisotano = models.BooleanField(default=False)
    azotea = models.BooleanField(default=False)
    responsable_obra = models.ForeignKey(ResponsableObra, on_delete=models.PROTECT)
    supervisor_obra = models.ForeignKey(SupervisorObra, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        supervisor_info = f" / Supervisor: {self.supervisor_obra}" if self.supervisor_obra else " / Sin supervisor"
        return f"Resolución: {self.resolucion} / Responsable: {self.responsable_obra}{supervisor_info}"

    class Meta:
        verbose_name = "Detalle de Resolución"
        verbose_name_plural = "Detalles de Resoluciones"
