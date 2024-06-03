from account.models import User, UserImage
from .serializers import UserDetailSerializer
from rest_framework import viewsets



class UserDetailViewSet(viewsets.ModelViewSet):
    '''User Detail'''
    serializer_class = UserDetailSerializer
  
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        queryset = User.objects.filter(slug=slug)
        return queryset
    
    

