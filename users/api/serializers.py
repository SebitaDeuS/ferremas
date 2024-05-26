from rest_framework import serializers
from appModelosDB.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    vendedor = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'vendedor']
    

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name','last_name','email']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['first_name','last_name','email']



