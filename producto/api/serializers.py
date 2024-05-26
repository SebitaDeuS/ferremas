from rest_framework import serializers
from appModelosDB.models import Producto, Promocion

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class PromocionSerializer(serializers.ModelSerializer):
    productos = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), many=True)
    descuento_porcentaje = serializers.FloatField(write_only=True, required=False)  # Nuevo campo

    class Meta:
        model = Promocion
        fields = '__all__'