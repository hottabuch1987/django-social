from account.models import User
from rest_framework import serializers


    
class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]
        user = User(
            email=email,
            username=username,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        read_only_fields = (
            'date_joined',
            'birth_date',
        ),
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'slug',
            'tel',     
            'friends',
            'likes',
            'online_status',
            'marital_status',
            'bio',
            'gender',
            'avatar',
                 
        )