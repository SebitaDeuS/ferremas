from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .serializers import ProductoSerializer, PromocionSerializer, HistorialPrecioSerializer
from appModelosDB.models import Producto, Promocion ,HistorialPrecio
from .permissions import IsAdminOrReadOnly


class ProductoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    

    @action(detail=True, methods=['post'])
    def ser_lanzamiento_reciente(self, request, pk=None):
        producto = self.get_object()
        producto.ser_lanzamiento_reciente()
        producto.save()
        return Response({'status': 'Producto marcado como lanzamiento reciente'})

    @action(detail=True, methods=['post'])
    def dejar_de_ser_lanzamiento_reciente(self, request, pk=None):
        producto = self.get_object()
        producto.dejar_de_ser_lanzamiento_reciente()
        producto.save()
        return Response({'status': 'Producto ya no es lanzamiento reciente'})
    

    @action(detail=True, methods=['post'])
    def salir_de_promocion(self, request, pk=None):
        producto = self.get_object()
        producto.salir_de_promocion()
        producto.save()
        return Response({'status': 'Producto ya no está en promoción'})
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Aquí guardamos el precio anterior si el precio ha cambiado
        if 'precio_producto' in serializer.validated_data and instance.precio_producto != serializer.validated_data['precio_producto']:
            historial_precio = HistorialPrecio.objects.create(producto=instance, precio_antiguo=instance.precio_producto)
            historial_precio.save()

        serializer.save()

        return Response(serializer.data)
    



class PromocionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer

    def perform_create(self, serializer):
        productos_nuevos = self.request.data.get('productos', [])
        descuento_porcentaje = self.request.data.get('descuento_porcentaje', 0)  # Asegúrate de recibir el descuento como parámetro

        # Verificar si los productos ya están en promoción
        productos_ya_en_promocion = Producto.objects.filter(id_producto__in=productos_nuevos, en_promocion=True)

        if productos_ya_en_promocion.exists():
            raise serializers.ValidationError("Algunos productos ya están en promoción.")

        # Guardar la promoción
        promocion = serializer.save()

        # Actualizar los productos para marcar que están en promoción y aplicar el descuento
        for producto_id in productos_nuevos:
            producto = Producto.objects.get(id_producto=producto_id)
            producto.entrar_en_promocion(descuento_porcentaje)
            producto.save()

        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        productos_nuevos = self.request.data.get('productos', [])

        # Guardar los cambios en la promoción
        promocion = serializer.save()

        # Obtener la lista de productos actualmente en la promoción
        productos_actuales = promocion.productos.all()

        # Verificar si la promoción está siendo deshabilitada
        if promocion.estado == 'deshabilitado':
            for producto in productos_actuales:
                producto.salir_de_promocion()
                producto.save()
        else:
            # Productos que ya están en la promoción pero no deberían estarlo
            productos_a_remover = productos_actuales.exclude(id_producto__in=productos_nuevos)
            for producto in productos_a_remover:
                producto.salir_de_promocion()
                producto.save()

            # Verificar si los productos nuevos ya están en otra promoción
            productos_ya_en_promocion = Producto.objects.filter(id_producto__in=productos_nuevos, en_promocion=True).exclude(promocion=promocion)
            if productos_ya_en_promocion.exists():
                raise serializers.ValidationError("Algunos productos ya están en promoción.")

            # Productos que son nuevos en la promoción
            productos_a_agregar = Producto.objects.filter(id_producto__in=productos_nuevos).exclude(id_producto__in=productos_actuales)
            for producto in productos_a_agregar:
                producto.entrar_en_promocion(promocion.descuento_porcentaje)
                producto.save()

            # Verificar si el porcentaje de descuento ha cambiado
            if promocion.descuento_porcentaje != instance.descuento_porcentaje:
                for producto in productos_actuales:
                    producto.salir_de_promocion()  # Restablecer el precio original
                    producto.entrar_en_promocion(promocion.descuento_porcentaje)  # Aplicar el nuevo descuento
                    producto.save()

        return super().perform_update(serializer)



