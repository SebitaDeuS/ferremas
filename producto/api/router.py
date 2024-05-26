from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, PromocionViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'promociones', PromocionViewSet, basename='promocion')

urlpatterns = router.urls