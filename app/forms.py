from .models import Friend, Message, Chat, GroupChat , Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False, label='Номер телефона')
    avatar = forms.ImageField(required=False, label='Аватарка')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        phone = self.cleaned_data.get('phone')
        avatar = self.cleaned_data.get('avatar')
        if commit:
            user.save()
            profile = Profile.objects.create(user=user, phone=phone)
            if avatar:
                profile.avatar = avatar
                profile.save()
        return user


class GroupChatForm(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields = ['name', 'participants']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['friend']

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return phone