from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserForm
from devproject.models import *
from django.contrib import messages,auth
# Create your views here.

def profile(request,pk):
    profile = Profile.objects.get(id=pk)
    rooms = profile.room_set.all()
    topics = Topics.objects.all()
    profile_messages = profile.messages_set.all()
    context = {'profile':profile,'rooms':rooms,'topics':topics,'profile_messages':profile_messages}
    return render(request,'devaccounts/profile.html',context)

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,'This username already exists.')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'This eamil already exists.')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(first_name=first_name,username=username,email=email,password=password)
                    user.save()
                    messages.success(request,'User registration is successfull.')
                    return redirect('home')
        else:
            messages.error(request,'Password Field does not matched')
            return redirect('signup')
    else:
        return render(request,'devaccounts/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'User login has been successfull')
            return redirect('home')
        else:
            messages.error(request,'Username or password is incorrect')
            return redirect('login')
    
    return render(request,'devaccounts/login.html')

@login_required(login_url='login')   
def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    form = UserForm(instance=profile)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'devaccounts/edit_profile.html',context)



    