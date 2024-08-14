from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_avatar/', null=True, blank=True, verbose_name='Аватарка')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')

    def __str__(self):
        return self.user.username


class Friend(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_friend', verbose_name='Пользователь')
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend', verbose_name='Друг')
    
            
    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'

    def __str__(self):
        return f"{self.profile.user.username} -> {self.friend.user.username}"



class Chat(models.Model):
    participants = models.ManyToManyField(Profile, related_name='chats', verbose_name='Участники')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='messages/files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')

class GroupChat(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название группы')
    participants = models.ManyToManyField(Profile, related_name='group_chats', verbose_name='Участники')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Групповой чат'
        verbose_name_plural = 'Групповые чаты'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
