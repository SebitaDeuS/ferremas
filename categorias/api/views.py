from rest_framework import viewsets
from appModelosDB.models import CategoriaProducto
from .serializers import CategoriaProductoSerializer
from categorias.api.permissions import IsAdminOrReadOnly
from rest_framework import generics
from appModelosDB.models import Producto, CategoriaProducto
from .serializers import ProductoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class CategoriaProductoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategoriaProductoSerializer
    queryset = CategoriaProducto.objects.all()
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def productos(self, request, slug=None):
        categoria = self.get_object()
        productos = categoria.producto_set.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)


