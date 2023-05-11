from django.shortcuts import render,redirect
from .models import Room,Topics,Messages
from django.db.models import Q
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