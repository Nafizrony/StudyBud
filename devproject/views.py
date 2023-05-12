from django.shortcuts import render,redirect
from .models import Room,Topics,Messages
from django.db.models import Q
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else  ''
    rooms = Room.objects.filter(
        Q(title__icontains=q)|
        Q(topic__name__icontains=q)|
        Q(description__icontains=q)
    )
    room_messages = Messages.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    topics = Topics.objects.all()
    context = {'rooms':rooms,'topics':topics,'room_messages':room_messages}
    return render(request,'devproject/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.messages_set.all()
    room_participants = room.participants.all()
    if request.method == 'POST':
        message = Messages.objects.create(
            user = request.user.profile,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user.profile)
        return redirect('room', room.id)
    context = {'room':room,'room_messages':room_messages,'room_participants':room_participants}
    return render(request,'devproject/room.html',context)

@login_required(login_url="login")
def create_room(request):
    form = RoomForm()
    topics = Topics.objects.all()
    if request.method == 'POST':
        topic_title = request.POST.get('topic')
        topic,created = Topics.objects.get_or_create(name=topic_title)
        Room.objects.create(
            host = request.user.profile,
            topic = topic,
            title = request.POST.get('title'),
            description = request.POST.get('description')
        )
        return redirect('home')
    context = {'form':form,'topics':topics}
    return render(request,'devproject/create_room.html',context)

@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topics.objects.all()
    if request.user != room.host:
        print('You are not allowed to update the room')
        return HttpResponse('You are not allowed to update the room')
        # messages.error(request,'You are not allowed to update the room')
    if request.method == 'POST':
        topic_title = request.POST.get('topic')
        topic,created = Topics.objects.get_or_create(name=topic_title)
        room.title = request.POST.get('title'),
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')
    context = {'form':form,'topics':topics}
    return render(request,'devproject/create_room.html',context)

@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        print('You are not allowed to delete the room')
        return HttpResponse('You are not allowed to delete the room')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room_obj':room}
    return render(request,'devproject/delete_room.html',context)

@login_required(login_url='login')
def delete_message(request,pk):
    message = Messages.objects.get(id=pk)
    if request.user != message.user:
        print('You are not allowed to delete the message')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'message_obj':message}
    return render(request,'devproject/delete_room.html',context)

def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topics.objects.filter(
        Q(name__icontains=q)
    )
    context = {'topics':topics}
    return render (request,'devproject/alltopics.html',context)


def activities(request):
    activities = Messages.objects.all()
    context = {'activities':activities}
    return render(request,'devproject/allactivities.html',context)
