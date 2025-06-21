from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_cart/<int:pk>/' , views.add_cart , name='add_cart'),
    path('cart/', views.view_cart , name='view_cart'),
    path('remove/<int:pk>/', views.remove_cartItem , name='remove'),
    path('checkout/', views.checkout , name='checkout'),
    path('place_order/', views.place_order , name='place_order'),
    path('category/<str:category_name>/', views.category_view , name='category')
]
