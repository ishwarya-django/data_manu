
from django.urls import path
from . import views



urlpatterns = [
    path('add_product/', views.add_product,name='add_product'),
    path('register/', views.register,name='register'),
    path('', views.login,name='login'),
    path('logout_view/', views.logout_view,name='logout_view'),
    path('sell_price/<int:id>/', views.sell_price,name='sell_price'),
    path('purchasepro/<int:id>/', views.purchasepro,name='purchasepro'),
    path('expense/<int:id>/', views.expense,name='expense'),
    path('layout/', views.layout,name='layout'),
    path('add_expense/', views.add_expense,name='add_expense'),
    path('index/', views.index,name='index'),

    
    




]
