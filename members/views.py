from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def login_user(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user  = authenticate(request,username=username,password=password)
        if user is not None:
            return redirect('home')
        else:
            messages.success(request,("User doesn't exists"))
            return redirect('login')
    else:
        return render(request,'authenticate/login_user.html',{})

