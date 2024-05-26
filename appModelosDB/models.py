from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from decimal import Decimal

# Create your models here.



class User(AbstractUser):
    vendedor = models.BooleanField(default=False)
    especialidad = models.CharField(max_length=50)

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    fec_pago = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)



class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    nomb_sucursal = models.CharField(max_length=255)
    direccion_sucursal = models.CharField(max_length=255)



class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    stock_sucursal = models.IntegerField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

  

class TipoProducto(models.Model):
    id_tp_producto = models.AutoField(primary_key=True)
    nomb_tp_producto = models.CharField(max_length=255)



class CategoriaProducto(models.Model):
    id_categoria_prod = models.AutoField(primary_key=True)
    nombre_categoria_prod = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre_categoria_prod)
        super(CategoriaProducto, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_categoria_prod


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nomb_producto = models.CharField(max_length=255)
    descrip_producto = models.TextField()
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    precio_original = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Nuevo campo
    marca_producto = models.CharField(max_length=255)
    modelo_producto = models.CharField(max_length=255)
    stock_total = models.IntegerField()
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    categoria_producto = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, null=True, blank=True)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    en_promocion = models.BooleanField(default=False)
    lanzamiento_reciente = models.BooleanField(default=False)
    categoria_original = models.ForeignKey(CategoriaProducto, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_originales')


    def entrar_en_promocion(self, descuento_porcentaje):
        if not self.en_promocion:
            self.categoria_original = self.categoria_producto
            self.categoria_producto = None
            self.precio_original = self.precio_producto
            self.precio_producto -= self.precio_producto * (Decimal(descuento_porcentaje) / Decimal(100))
            self.en_promocion = True
            self.save()

    def salir_de_promocion(self):
        if self.en_promocion:
            self.categoria_producto = self.categoria_original
            self.categoria_original = None
            self.precio_producto = self.precio_original
            self.precio_original = None
            self.en_promocion = False
            self.save()

    def ser_lanzamiento_reciente(self):
        if not self.lanzamiento_reciente:
            self.categoria_original = self.categoria_producto
            self.categoria_producto = None
            self.lanzamiento_reciente = True
            self.save()

    def dejar_de_ser_lanzamiento_reciente(self):
        if self.lanzamiento_reciente:
            self.categoria_producto = self.categoria_original
            self.categoria_original = None
            self.lanzamiento_reciente = False
            self.save()
    
    def __str__(self):
        return self.nomb_producto

class HistorialPrecio(models.Model):
    id_historial = models.AutoField(primary_key=True)
    precio_antiguo = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.precio_antiguo

class Promocion(models.Model):
    codigo_promocion = models.AutoField(primary_key=True)
    nombre_promocion = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    productos = models.ManyToManyField(Producto)
    descuento_porcentaje = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre_promocion



class DetalleBoleta(models.Model):
    id_boleta = models.AutoField(primary_key=True)
    fecha_boleta = models.DateField()
    total_boleta = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)




class ChatConsulta(models.Model):
    id_consulta = models.AutoField(primary_key=True)
    asunto = models.CharField(max_length=255)
    mensaje = models.TextField()
    respuesta = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    