from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from appModelosDB.models import User, Pago, Sucursal, Inventario, TipoProducto, CategoriaProducto, Producto, HistorialPrecio, Promocion, DetalleBoleta, ChatConsulta

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(Pago)
admin.site.register(Sucursal)
admin.site.register(Inventario)
admin.site.register(TipoProducto)
admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(HistorialPrecio)
admin.site.register(Promocion)
admin.site.register(DetalleBoleta)
admin.site.register(ChatConsulta)



