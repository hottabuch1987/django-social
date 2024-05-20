from account.models import User
from django.shortcuts import render

from .models import ChatModel



def index(request):
    user = request.user
    users = User.objects.filter(friends=user).exclude(id=request.user.id)
    return render(request, 'direct_messages/conversation.html', context={'users': users})


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
