
from django.shortcuts import render , redirect,get_object_or_404
from pydantic import ValidationError
from .forms import  FriendRequestForm , CustomUserCreationForm , ProfileForm
from .models import Friend , Chat, Message , Profile 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def index(request):
    profile = Profile.objects.get(user=request.user)
    friends = Friend.objects.filter(profile=profile)
    context = {"friends" : friends}
    return render(request, 'index.html' , context)

# Регистрация и аутентификация 
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {"form": form})



def login_site(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username,password=password)
        if user is not None:
            login(request, user=user)
            return redirect('index')
        else:
            return render(request, 'index.html' , {"error" : "неверное имя или пароль"})
    return render(request, "login.html")


def logout_site(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')
# ------------------------------------------------------

# Добавление в друзья
@login_required
def send_friend_request(request):
    if request.method == 'POST':
        form = FriendRequestForm(request.POST)
        if form.is_valid():
            friend_request = form.save(commit=False)
            friend_request.user = request.user
            friend_request.save()
            return redirect('friends_list')
    else:
        form = FriendRequestForm()
    return render(request, 'send_friend_request.html', {'form': form})



def get_or_create_chat(user1, user2):
    profile1 = user1.profile
    profile2 = user2.profile
    chat = Chat.objects.filter(participants=profile1).filter(participants=profile2).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(profile1, profile2)
    return chat

@csrf_exempt
@login_required
def send_message(request, friend_id):
    if request.method == 'POST':
        user = request.user
        friend = get_object_or_404(User, id=friend_id)
        content = request.POST.get('content')
        file = request.FILES.get('file')

        # Получение или создание чата
        chat = get_or_create_chat(user, friend)

        if content or file:
            message = Message.objects.create(
                sender=user,
                receiver=friend,
                content=content,
                file=file,
                timestamp=timezone.now(),
                chat=chat
            )
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    data = {
        'username': profile.user.username,
        'avatar': profile.avatar.url if profile.avatar else 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png',
        'phone': profile.phone or 'Not provided'
    }
    return JsonResponse(data)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            try:
                form.save()
                return redirect('index')
            except ValidationError as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile view
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})

def search_users(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        users = Profile.objects.filter(userusernameicontains=query)
        results = [{'id': user.user.id, 'username': user.user.username, 'avatar': user.avatar.url if user.avatar else None} for user in users]
        return JsonResponse({'users': results})


@login_required
def add_friend(request, user_id):
    user_to_add = get_object_or_404(User, id=user_id)
    if user_to_add != request.user:
        profile = request.user.profile
        friend_profile = user_to_add.profile


        if not Friend.objects.filter(profile=profile, friend=friend_profile).exists():

            Friend.objects.create(profile=profile, friend=friend_profile)
            
           
            Friend.objects.get_or_create(profile=friend_profile, friend=profile)


            chat, created = Chat.objects.get_or_create(
                participants__in=[profile, friend_profile]
            )
            if created:
                chat.participants.add(profile, friend_profile)
                chat.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))

def chat_history(request, friend_id):
    if request.method == 'GET':
        profile = request.user.profile
        friend_profile = get_object_or_404(Profile, user_id=friend_id)
        chat = get_or_create_chat(request.user, friend_profile.user)

        messages = Message.objects.filter(chat=chat).order_by('timestamp')

        messages_data = [
            {
                'content': msg.content,
                'file': msg.file.url if msg.file else None,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_sender': msg.sender == request.user,
            }
            for msg in messages
        ]

        return JsonResponse({'messages': messages_data})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_chat(request, chat_id):
    if request.method == 'GET':
        chat = get_object_or_404(Chat, id=chat_id)
        messages = Message.objects.filter(chat=chat).order_by('timestamp')

    messages_data = [
        {
            'content': msg.content,
            'file': msg.file.url if msg.file else None,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_sender': msg.sender == request.user.profile,
        }
        for msg in messages
    ]

    return JsonResponse({'messages': messages_data})


