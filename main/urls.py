from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/filter/', views.filter_products, name='filter_products'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('enter/', views.enter, name='enter'),
    path('enter/add/', views.add_enter, name='add_enter'),
    path('enter/<int:enter_id>/', views.enter_item, name='enter_item'),
    path('enter/<int:enter_id>/add/', views.add_enter_item, name='add_enter_item'),
    path('enter/<int:enter_item_id>/edit/', views.edit_enter_item, name='edit_enter_item'),
    path('enter/filter/', views.filter_enter, name='filter_enter'),
    path('enter/<int:enter_id>/filter/', views.filter_enter_item, name='filter_enter_item'),
    path('out/', views.out, name='out'),
    path('out/add/', views.add_out, name='add_out'),
    path('out/<int:out_id>/', views.out_item, name='out_item'),
    path('out/<int:out_id>/add/', views.add_out_item, name='add_out_item'),
    path('out/item/<int:out_item_id>/edit/', views.edit_out_item, name='edit_out_item'),
    path('out/<int:out_id>/filter/', views.filter_out_item, name='filter_out_item'),
    path('out/filter/', views.filter_out, name='filter_out'),
]