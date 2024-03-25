from django.urls import path
from . import views

app_name = 'admins'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_book/', views.create, name='create'),
    path('view_book/<int:book_id>/', views.view, name='view'),
    path('edit/<int:book_id>/', views.edit, name='edit'),
    path('delete/<int:book_id>/', views.delete, name='delete'),
]


