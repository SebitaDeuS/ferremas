from rest_framework import generics
from appModelosDB.models import ChatConsulta
from .serializers import ChatConsultaSerializer
from rest_framework.permissions import IsAuthenticated

class ChatConsultaListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = ChatConsulta.objects.all()
    serializer_class = ChatConsultaSerializer

class ChatConsultaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = ChatConsulta.objects.all()
    serializer_class = ChatConsultaSerializer