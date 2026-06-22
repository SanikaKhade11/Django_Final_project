from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from base.models import Cart

# Create your views here.

def login_(request):
    if request.method == 'POST':
        u = authenticate(
            username = request.POST['username'],
            password = request.POST['password']
        )
        if u:
            login(request,u)
            return redirect('home')
        else:
            return render(request, 'login_.html',{'error': 'Username and Password are incorrect'})
    return render(request,'login_.html')

# @login_required(login_url='login_')
def register(request):
    if request.method == 'POST':
        try:
            u = User.objects.get(username = request.POST['username'])
            return render(request , 'register.html' ,{'error': 'Username already exists'})
        except:
            u = User.objects.create(
                first_name = request.POST['fname'],
                last_name = request.POST['lname'],
                email = request.POST['email'],
                username = request.POST['username']
            )
            u.set_password(request.POST['password'])
            u.save()
            return redirect('login_')
    
    return render(request,'register.html')

@login_required(login_url='login_')
def profile(request):
    cartproductCount = Cart.objects.filter(host = request.user).count()
    
    return render(request,'profile.html', {'cartproductCount':cartproductCount})

@login_required(login_url='login_')
def updateProfile(request):
    data = request.user
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']

        data.first_name = fname
        data.last_name = lname
        data.email = email
        data.save()
        return redirect('profile')

    return render(request,'updateProfile.html')

def logout_(request):
    logout(request)
    return redirect('login_')

