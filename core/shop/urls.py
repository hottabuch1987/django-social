from  django.urls import path
from  .views import search_products, ProductListView

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),

    path("search_products/", search_products, name="search-products"),
    #

]
