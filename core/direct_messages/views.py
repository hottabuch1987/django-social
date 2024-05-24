from account.models import User
from django.shortcuts import render
from random import choice
from .models import ChatModel
from django.db.models import Subquery


def index(request):
    user = request.user
  
    users = User.objects.filter(friends=user).exclude(id=request.user.id).order_by('?')

    not_friends = User.objects.exclude(id=user.id).exclude(id__in=Subquery(users.values('id'))).order_by('?')

    random_friend = choice(list(not_friends)) if not_friends else None


    return render(request, 'direct_messages/conversation.html', context={'users': users,  'random_friend': random_friend})


def chatPage(request, username):
    user_obj = User.objects.get(username=username)
    user = request.user
    users = User.objects.filter(friends=user)

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    message_objs = ChatModel.objects.filter(thread_name=thread_name)
    return render(request, 'direct_messages/send_message.html', context={'user': user_obj, 'users': users, 'messages': message_objs})
