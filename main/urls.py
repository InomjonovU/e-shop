from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movement/', views.movement, name='movement'),
    path('products/', views.products, name='products'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/filter/', views.filter_products, name='filter_products'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('movement/add/', views.add_movement, name='add_movement'),
    path('movement/filter/', views.movement_filter, name='movement_filter'),
]