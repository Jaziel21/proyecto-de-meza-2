from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Autor(models.Model):
    autorid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    fechanacimiento = models.DateField()
    bibliografia = models.TextField()
    paginaweb = models.URLField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Editorial(models.Model):
    editorialid = models.AutoField(primary_key=True)
    nombreeditorial = models.CharField(max_length=255, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    emailcontacto = models.EmailField(max_length=255)
    sitioweb = models.URLField(max_length=255, blank=True, null=True)
    paisorigen = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"
        ordering = ['nombreeditorial']
    
    def __str__(self):
        return self.nombreeditorial

class Cliente(models.Model):
    clienteid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    fecharegistro = models.DateTimeField(default=timezone.now)
    preferenciasgenero = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Libro(models.Model):
    GENEROS = [
        ('FIC', 'Ficción'),
        ('ROM', 'Romance'),
        ('TER', 'Terror'),
        ('CIE', 'Ciencia Ficción'),
        ('FAN', 'Fantasía'),
        ('HIS', 'Histórico'),
        ('BIO', 'Biografía'),
        ('INF', 'Infantil'),
        ('POE', 'Poesía'),
        ('DRA', 'Drama'),
    ]
    
    libroid = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=17, unique=True)
    anioPublicacion = models.IntegerField()
    genero = models.CharField(max_length=100, choices=GENEROS)
    precioventa = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']
    
    def __str__(self):
        return self.titulo
    
    def disponible(self):
        return self.stock > 0

class Venta(models.Model):
    ESTADOS_VENTA = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
        ('EN_PROCESO', 'En Proceso'),
    ]
    
    METODOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('DIGITAL', 'Pago Digital'),
    ]
    
    ventaid = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fechaventa = models.DateTimeField(default=timezone.now)
    montototal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodopago = models.CharField(max_length=50, choices=METODOS_PAGO)
    estadoVenta = models.CharField(max_length=50, choices=ESTADOS_VENTA, default='PENDIENTE')
    descuentoAplicado = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fechaventa']
    
    def __str__(self):
        return f"Venta #{self.ventaid} - {self.cliente}"

class DetalleVenta(models.Model):
    detalleDeLaVentaid = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precioUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0.16)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Ventas"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precioUnitario
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Detalle {self.detalleDeLaVentaid} - Venta {self.venta.ventaid}"