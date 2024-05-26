from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .serializers import ProductoSerializer, PromocionSerializer
from appModelosDB.models import Producto, Promocion
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
    




    



