from django.contrib.auth import authenticate, login, logout
from account.models import User, Forum, UserImage, Notification
from recommend.models import Review
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .tasks import send_registration_email, send_forum_message
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from .forms import LoginForm, UserCreateForm, UserUpdateForm,  ForumForm, UserImageForm
from django.db.models import Q
from django.contrib import messages
from django_email_verification import send_email
from django.http import JsonResponse
from random import choice



#Register new user
def register_user(request):

    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            user_email=form.cleaned_data.get('email')
            user_username=form.cleaned_data.get('username')
            user_password=form.cleaned_data.get('password1')

            #Create new user
            user = User.objects.create_user(
                username=user_username, email=user_email, password=user_password
            )

            user.is_active = False
            

            send_email(user)
            
            return redirect('/account/email-verification-sent/')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form}) 


def login_user(request):

    form = LoginForm()

    if request.user.is_authenticated:
        
        return redirect('shop:products')

    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        else:
            messages.info(request, 'Имя пользователя или пароль неверны')
            return redirect('account:login')
    context = {
        'form': form
    }
    return render(request, 'account/login/login.html', context)


def logout_user(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        if key == 'session_key':
            continue
        del request.session[key]
    logout(request)
    return redirect('account:login')


#my profile
@method_decorator(login_required, name='dispatch')
class DashboardUserView(View):
    template_name = 'account/dashboard/dashboard.html'

    def get(self, request):
        if request.user.is_authenticated:
            images = UserImage.objects.filter(user=request.user)

            

            all_friends = User.objects.all().exclude(id=request.user.id)
            random_friend = choice(all_friends) if all_friends else None
            friends = User.objects.filter(id=random_friend.id) if random_friend else None


            notifications = Notification.objects.filter(is_read=False).order_by('-timestamp')
            for notification in notifications:
                notification.is_read = True
                notification.save()

            recommendations = Review.objects.all().order_by('-created_at')
            context = {'friends': friends, 'notifications':notifications, 'recommendations':recommendations, 'images': images}
            return render(request, self.template_name, context)

    def post(self, request):
        friend_id = request.POST.get('friend_id')
        user = request.user
        friend = User.objects.get(id=friend_id)
        
        if 'method' in request.POST and request.POST['method'] == 'DELETE':
            # Remove friend
            user.friends.remove(friend)
            user.friends_count -= 1
            user.save()

            friend_count = user.friends_count
            data = {'friendCount': friend_count}  # Отправляем обновленное количество друзей в формате JSON
            Notification.objects.create(receiver=friend, sender=user, message=f"{user.username} удалил Вас из друзей ")

            return JsonResponse(data)
            
        else:
            # Add friend
            user.friends.add(friend)
            user.friends_count += 1
            user.save()
            friend_count = user.friends_count
            data = {'friendCount': friend_count}  # Отправляем обновленное количество друзей в формате JSON
            Notification.objects.create(receiver=friend, sender=user, message=f"{user.username}  добавил Вас в друзья")
            return JsonResponse(data)
        

#update my profile
@login_required(login_url='account:login')
def profile_user(request):
    user_form = UserUpdateForm(instance=request.user)
    images_form = UserImageForm(instance=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        images_form = UserImageForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid() and images_form.is_valid():
            user_instance = user_form.save()
            # Получаем или создаем объект изображения пользователя
            image_instance, created = UserImage.objects.get_or_create(user=request.user)
            image_instance.image = images_form.cleaned_data['image']
            image_instance.save()
            

            return redirect('account:dashboard')
    
    context = {
        'user_form': user_form,
        'images_form': images_form
    }
    
    return render(request, 'account/dashboard/profile-management.html', context)



#delete my profile
@login_required(login_url='account:login')
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('shop:products')
    return render(request, 'account/dashboard/account-delete.html')


#profiles detail other user
def user_detail(request, slug):
    user = get_object_or_404(User, slug=slug)
    
    
    images = UserImage.objects.filter(user=user)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if user.reviews.filter(created_by=request.user).exists():
                messages.error(request, 'Вы уже оставляли комментарий.')
            else:
                rating = request.POST.get('rating', 3)
                content = request.POST.get('content', '')
                if content:
                    user.reviews.create(rating=rating, content=content, created_by=request.user, user=user)
                    
                    messages.success(request, 'Ваш комментарий успешно добавлен.')
                    return redirect(request.path)
            #add and del fiends
            if user != request.user:
                if 'add_friend' in request.POST:
                    if request.user.friends.filter(id=user.id).exists():
                        messages.error(request, 'Этот пользователь уже у вас в друзьях!')
                    else:
                        request.user.friends.add(user)
                        request.user.save()
                        Notification.objects.create(sender=request.user, receiver=user, message=f"{request.user.username} добавил Вас в друзья")

                elif 'remove_friend' in request.POST:
                    if request.user.friends.filter(id=user.id).exists():
                        request.user.friends.remove(user)
                        request.user.save()
                        Notification.objects.create(sender=request.user, receiver=user, message=f"{request.user.username} удалил Вас из друзей")
                return redirect('account:user_detail', slug=slug)
            #likes
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.user.is_authenticated:
        if user.likes.filter(id=request.user.id).exists():
            user.likes.remove(request.user)
            user.like_count -= 1
        else:
            user.likes.add(request.user)
            user.like_count += 1

        user.save()

        data = {
            'like_count': user.like_count
        }
        return JsonResponse(data)

    context = {'user': user, 'images': images}
    return render(request, 'account/dashboard/users_detail.html', context)
#rewiews
# def reviews(request):
#     """Обратная связь"""
#     if request.method == "POST":
#         form = ReviewsForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse(status=204)
#     else:
#         form = ReviewsForm()
#     return render(request, 'account/modal/reviews.html', {
#         'form': form,
#     })


#forum
class ForumView(View):
    def get(self, request, *args, **kwargs):
        form = ForumForm()
        forums = Forum.objects.all()
        return render(request, 'account/dashboard/send_message.html', {'form': form, 'forums': forums})

    def post(self, request, *args, **kwargs):
        form = ForumForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user  # Присваивание отправителя перед сохранением
            message.receiver_id = form.cleaned_data.get('receiver_id')
            message.save()
            # Запуск асинхронной задачи Celery для отправки сообщения
            send_forum_message.delay(message.id)
            return redirect('account:forum_message')
        else:
            form = ForumForm()
            error = messages.info(request, 'Возникла ошибка при отправке сообщения')
       
            return render(request, 'account/dashboard/send_message.html', {'form': form, 'error': error})

 