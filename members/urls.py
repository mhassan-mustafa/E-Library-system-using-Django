from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('view/<int:book_id>/', views.view, name='view'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('register/', views.register, name='register'),
    path('verify/<int:account_id>/', views.verify, name='verify'),
    path('request_book/<int:book_id>/', views.request_book, name='request'),
]