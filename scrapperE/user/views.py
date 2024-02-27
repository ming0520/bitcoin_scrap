from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import logout
# Create your views here.
 
def register(request):
    if request.method== 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, find your job today!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'user/register.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('logout_msg')

def logout_msg(request):
    return render(request,'user/logout.html')