from django.urls import path
from .views import ChatConsultaListCreate, ChatConsultaRetrieveUpdateDestroy

urlpatterns = [
    path('consultas/', ChatConsultaListCreate.as_view(), name='consulta-list-create'),
    path('consultas/<int:pk>/', ChatConsultaRetrieveUpdateDestroy.as_view(), name='consulta-retrieve-update'),
]