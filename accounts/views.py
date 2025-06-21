from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.


def singup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request  , user)
            messages.success(request , 'Signup Successful')
            return redirect ('login')
    else:
        form = UserCreationForm()
    return render(request , 'signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username = username , password = password)
        if user:
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , "Invalid login username")
    return render(request , 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
