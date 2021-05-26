from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login),
    path('signup/', views.signup),
    path('accounts/', views.get_accounts),
    path('accounts/<int:pk>/', views.get_account),
    path('accounts/delete/<int:pk>/', views.delete_account),

]
