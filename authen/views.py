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

def resetPass(request):
    user = request.user
    if request.method == 'POST':
        if 'old_pass' in request.POST:
            old = request.POST['old_pass']

            u = authenticate(username = user.username, password = old)
            if u:
                return render(request, 'resetPass.html', {'new_pass': True})
            else:

                return render(request, 'resetPass.html', {'error': 'Old password is incorrect'})
        
        if 'new_pass' in request.POST:
            new = request.POST['new_pass']

            if user.check_password(new):
                return render(request, 'resetPass.html', {'error': 'New Password Cannot Be Same As Old password'})
            user.set_password(new)
            user.save()
            return redirect('login_')
      
    return render(request, 'resetPass.html')

def forgetPass(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            u = User.objects.get(username = username)
            request.session['fp_user'] = u.username
            return redirect('new_password')
        except:
            return render(request,'forgotpass.html',{'error':'Invalid Username'})

    return render(request, 'forgetPass.html')

def new_password(request):
    username=request.session.get('fp_user')
    if username is None:
        return redirect('forgetpass')
    user=User.objects.get(username=username)
    if request.method == 'POST':
        new_pass=request.POST['new']
        if user.check_password(new_pass):
            return render(request,'newpass.html',{'error':'New password should not be similar as old password'})
        user.set_password(new_pass)
        user.save()
        #remove the username from the session storage
        del request.session['fp_user']
        return redirect('login_')
    return render(request,'newpass.html')


