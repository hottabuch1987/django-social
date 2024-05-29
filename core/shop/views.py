from django.shortcuts import render, get_object_or_404, redirect
from account.models import User
from django.views.generic import ListView
from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.db.models import Q
from random import choice



class ProductListView(ListView):
    model = User
    context_object_name = "products"
    paginate_by = 10

   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = User.objects.all().exclude(id=self.request.user.id)
        return context

    def get_template_names(self):
        if self.request.htmx:
            return ["shop/components/product_list.html"]
        return ["shop/products.html"]
    
from datetime import datetime

# Функция для расчета возраста по дате рождения
def calculate_age(birth_date):
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Функция для поиска  с фильтрацией по возрасту, полу и онлайн-статусу
# Функция для поиска с фильтрацией по возрасту, полу и онлайн-статусу
def search_products(request):
    query = request.GET.get('q')
    gender = request.GET.get('gender')
    online_status = request.GET.get('online_status') 
    
    if gender:
        users = User.objects.filter(gender=gender)  # Assuming User model exists

    elif online_status == 'online':  # Check if 'online_status' is 'online'
        users = User.objects.filter(online_status=True)
    else:
        users = User.objects.all()  # Or any default queryset
    
    context = {'users': users.distinct()}  # Assuming you want to pass users data to template
    return render(request, 'shop/products.html', context)



def error_404(request, exception):
    return render(request, '404.html')

def error_403(request, exception):
    return render(request, '403.html')



