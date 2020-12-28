from django.shortcuts import render,redirect
from django.http import HttpResponse
from users_app.form import UserForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            userform.save()
            messages.success(request,"USER REGISTERED!")
            return redirect('home')
        else:
            messages.success(request,"USER NOT REGISTERED!")
            return redirect('register')     
    else:
        userform = UserForm()
        return render(request,'register.html',{'userform':userform})





    
    

    