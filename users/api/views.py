from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from users.api.serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer
from appModelosDB.models import User

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)


        if serializer.is_valid(raise_exception=True):
            vendedor = serializer.validated_data.get('vendedor', False)
            if vendedor:
                # Aquí puedes implementar la lógica para asignar permisos adicionales a los vendedores
                print("Es vendedor")
            serializer.save()
            return Response(serializer.data)
            
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Obtener el usuario autenticado
        serializer = UserSerializer(user)  # Pasar el objeto de usuario al serializador
        return Response(serializer.data)



    def put(self, request):
        #request.user.id

        user = User.objects.get(id=request.user.id)
        serializer = UserUpdateSerializer(user, request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
