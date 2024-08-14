from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.index , name='index'),
    path('register/', views.register_view, name='register'),
    path("", views.login_site , name='login_site'),
    path('logout/' , views.logout_site, name='logout_site'),
    path('chats/<int:friend_id>/', views.chat_history, name='chat_history'),
    path('chats/<int:friend_id>/send/', views.send_message, name='send_message'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search/', views.search_users, name='search_users'),
    path('add_friend/<int:user_id>/', views.add_friend, name='add_friend'),
]

