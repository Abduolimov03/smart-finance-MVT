from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_home, name='expense_home'),
    path('add/', views.expense_add, name='expense_add'),
    path('update/<int:pk>/', views.expense_update, name='expense_update'),
    path('delete/<int:pk>/', views.expense_delete, name='expense_delete'),
]
