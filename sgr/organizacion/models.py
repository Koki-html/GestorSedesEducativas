from django.contrib.auth.models import Group, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


STATUS_CHOICES = (
    ('activo', 'Activo'),
    ('inactivo', 'Inactivo'),
    ('terminado', 'Terminado'),
)


class Sector(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class SedeEducativa(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    encargado = models.ForeignKey(
        'UsuarioColaborador',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sedes_encargadas',
    )
    sector = models.ForeignKey(
        Sector,
        on_delete=models.PROTECT,
        related_name='sedes',
    )
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Cargo(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Rol(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    grupo = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        related_name='roles_sistema',
    )
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class UsuarioColaborador(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_colaborador',
    )
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    rut = models.CharField(max_length=20, unique=True)
    correo = models.EmailField()
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        related_name='colaboradores',
    )
    sede = models.ForeignKey(
        SedeEducativa,
        on_delete=models.PROTECT,
        related_name='colaboradores',
    )
    roles = models.ManyToManyField(Rol, related_name='colaboradores', blank=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    @property
    def ultimo_acceso(self):
        return self.usuario.last_login

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'


class Solicitante(models.Model):
    rut = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30)
    correo = models.EmailField()
    direccion = models.CharField(max_length=255)
    sector = models.ForeignKey(
        Sector,
        on_delete=models.PROTECT,
        related_name='solicitantes',
    )
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'


class ComiteSede(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    sede = models.ForeignKey(SedeEducativa, on_delete=models.PROTECT, related_name='comites')
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name='comites')
    fecha_constitucion = models.DateField()
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ParticipacionComite(models.Model):
    solicitante = models.ForeignKey(Solicitante, on_delete=models.PROTECT, related_name='participaciones')
    comite = models.ForeignKey(ComiteSede, on_delete=models.CASCADE, related_name='participaciones')
    es_coordinador = models.BooleanField(default=False)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, related_name='participaciones')
    fecha_incorporacion = models.DateField()
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.solicitante} - {self.comite}'


class HitoMantenimiento(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    periodicidad = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(null=True, blank=True)
    sede = models.ForeignKey(SedeEducativa, on_delete=models.PROTECT, related_name='hitos')
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name='hitos')
    responsables = models.ManyToManyField(
        UsuarioColaborador,
        related_name='hitos',
        blank=True,
    )
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Espacio(models.Model):
    sede = models.ForeignKey(SedeEducativa, on_delete=models.PROTECT, related_name='espacios')
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.sede.nombre} - {self.nombre}'


class TipoServicio(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class SubtipoServicio(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    tipo = models.ForeignKey(TipoServicio, on_delete=models.PROTECT, related_name='subtipos')
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.tipo.nombre} - {self.nombre}'
