from account.models import User, UserImage, Forum
from .serializers import UserDetailSerializer, ForumSerializer, AllUsersSerializer
from rest_framework import viewsets
from .tasks import get_user_queryset_async



class UserDetailViewSet(viewsets.ModelViewSet):
    '''User Detail'''
    serializer_class = UserDetailSerializer
  
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        async_result = get_user_queryset_async.delay(slug)
        queryset = async_result.get()

        return queryset
class ForumViewSet(viewsets.ModelViewSet):  
    '''Forum'''  
    serializer_class = ForumSerializer
    queryset = Forum.objects.all()


class AllUsersViewSet(viewsets.ModelViewSet):
    '''All Users and Search'''
    serializer_class = AllUsersSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        gender = self.request.query_params.get('gender')
        online_status = self.request.query_params.get('online_status')
        marital_status = self.request.query_params.get('marital_status')

        if gender:
            queryset = queryset.filter(gender=gender)
        if online_status == 'online':
            queryset = queryset.filter(online_status=True)
        if marital_status == 'married':
            queryset = queryset.filter(marital_status='married')
        elif marital_status == 'searching':
            queryset = queryset.filter(marital_status='searching')
        elif marital_status == 'single':
            queryset = queryset.filter(marital_status='single')

        return queryset
    


