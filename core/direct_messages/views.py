from account.models import User
from django.shortcuts import render
from random import randint
from .models import ChatModel
from django.db.models import Subquery
import re

def index(request):
    user = request.user
  
    users = User.objects.filter(friends=user).exclude(id=request.user.id).order_by('?')

    not_friends = User.objects.exclude(id=user.id).exclude(id__in=Subquery(users.values('id'))).order_by('?')



    return render(request, 'direct_messages/conversation.html', context={'users': users,  'not_friends': not_friends})




def convert_guid_to_number(guid):
        # Преобразование UUID в строку и удаление дефисов
        guid_str = str(guid).replace('-', '')
        guid_digits = re.sub(r'\D', '', guid_str)
        number_value = int(guid_digits)
        return number_value

def chatPage(request, username):
    user_obj = User.objects.get(username=username)

    user = request.user
    users = User.objects.filter(friends=user)
  

    if convert_guid_to_number(request.user.id) > convert_guid_to_number(user_obj.id):
      
        thread_name = f'chat_{str(convert_guid_to_number(request.user.id))}-{str(convert_guid_to_number(user_obj.id))}'
    else:
        thread_name = f'chat_{str(convert_guid_to_number(user_obj.id))}-{str(convert_guid_to_number(request.user.id))}'
    
 
    
    message_objs = ChatModel.objects.filter(thread_name=thread_name)

    return render(request, 'direct_messages/send_message.html', context={'user': user_obj, 'users': users, 'messages': message_objs})
