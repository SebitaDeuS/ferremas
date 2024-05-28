from rest_framework import serializers
from appModelosDB.models import ChatConsulta

class ChatConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatConsulta
        fields = '__all__'