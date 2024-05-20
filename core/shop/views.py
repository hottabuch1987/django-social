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
    



#поиск на ru-en языках в названии и описании
def search_products(request):
    query = request.GET.get('q')
    if not query:
        return redirect('shop:products')

    products = User.objects.filter(
        Q(title_ru__icontains=query) |
        Q(title_en__icontains=query) |
        Q(description_content_ru__icontains=query) |
        Q(description_content_en__icontains=query)
    ).distinct()

    context = {'products': products}
    return render(request, 'shop/products.html', context)




def error_404(request, exception):
    return render(request, '404.html')

def error_403(request, exception):
    return render(request, '403.html')



