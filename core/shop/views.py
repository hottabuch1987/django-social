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
    


# Функция для поиска  с фильтрацией по возрасту, полу и онлайн-статусу

from datetime import datetime, timedelta, date

def search_products(request):
    query = request.GET.get('q')
    gender = request.GET.get('gender')
    online_status = request.GET.get('online_status')
    marital_status = request.GET.get('marital_status')
    age_query = request.GET.get('birth_date')


    users = User.objects.all()


        

    if gender and online_status == 'online':
        users = users.filter(gender=gender, online_status=True)
    if marital_status == 'married':
        users = users.filter(marital_status='married')
    if marital_status == 'searching':
        users = users.filter(marital_status='searching')
    if marital_status == 'single':
        users = users.filter(marital_status='single')
    if online_status == 'online':
        users = users.filter(online_status=True)
    if gender:
        users = users.filter(gender=gender)
    age_query = request.GET.get('birth_date')
    age_query_max = request.GET.get('birth_date_max')

    if age_query:
        current_date = date.today()

        min_age = int(age_query)
        max_age = int(age_query_max)

        birth_date_max = current_date.replace(year=current_date.year - min_age)
        birth_date_min = current_date.replace(year=current_date.year - max_age)

        users = users.filter(birth_date__gte=birth_date_min, birth_date__lte=birth_date_max)



    context = {'users': users.distinct()}  # Assuming you want to pass users data to template
    return render(request, 'shop/products.html', context)



def error_404(request, exception):
    return render(request, '404.html')

def error_403(request, exception):
    return render(request, '403.html')



