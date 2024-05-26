from rest_framework import serializers
from appModelosDB.models import CategoriaProducto
from producto.api.serializers import ProductoSerializer


class CategoriaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProducto
        fields = '__all__'

class CategoriaProductoSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True, read_only=True)  # Utiliza el serializer de producto

    class Meta:
        model = CategoriaProducto
        fields = ['id_categoria_prod', 'nombre_categoria_prod', 'productos']