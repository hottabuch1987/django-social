from account.models import User, UserImage, Forum
from rest_framework import serializers


    
class CustomUserCreateSerializer(serializers.ModelSerializer):
    '''Создание пользователя'''
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

class AllUsersSerializer(serializers.ModelSerializer):
    '''Список всех пользователей'''
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'online_status', 'gender', 'slug'] 

        

class UserImageSerializer(serializers.ModelSerializer):
    ''''Детали пользователя'''
    class Meta:
        model = UserImage
        fields = ['image', 'user']


class UserDetailSerializer(serializers.ModelSerializer):

    avatar = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'bio', 
            'date_joined', 
            'birth_date', 
            'avatar', 
            'gender', 
            'tel', 
            'friends', 
            'friends_count', 
            'online_status', 
            'likes', 
            'like_count', 
            'slug', 
            'marital_status', 
            'user_image'
        ]

    def get_avatar(self, obj):
        if isinstance(obj, dict):
            return obj['avatar']
        return obj.get_avatar()
    
    def get_user_image(self, obj):
        if isinstance(obj, dict):
            user_id = obj.get('id')
        else:
            user_id = obj.id

        user_image_obj = UserImage.objects.filter(user=user_id).first()
        if user_image_obj:
            return UserImageSerializer(user_image_obj).data
        return None


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = [
            'sender',
            'receiver',
            'content',
            'timestamp',
            'message_file'
        ]


