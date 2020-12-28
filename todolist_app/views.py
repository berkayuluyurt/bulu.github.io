from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import tasklist
from todolist_app.form import taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render
from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User , auth
from datetime import datetime
from datetime import date
import json
import time
import sqlite3 
# Create your views here.
def home(Response):
    return render(Response,'home.html')

def deletetask(Response,task_id):
    print(Response)
    task = tasklist.objects.get(pk=task_id)
    if task.manage == Response.user:
        task.delete()
        return redirect('todolist')
    else:
        return redirect('home')    

def comppend(Response,task_id):
    task = tasklist.objects.get(pk=task_id)
    if task.manage == Response.user:
        if task.done:
            task.done = False
            task.point-=int(task.priority)
            task.end_at=None
            task.end_on=None
        else:
            task.done = True
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            today = date.today()
            current_date = today.strftime("%Y-%m-%d")
            end_on = current_date
            end_at = current_time  
            task.end_at =end_at 
            task.end_on =end_on
            task.point += int(task.priority)           
        task.save()    
        return redirect('todolist')
    else:
        return redirect('home')        

def edittask(Response,task_id):
    
    if Response.method == "POST":
        task = tasklist.objects.get(pk=task_id)
        form = taskform(Response.POST or None,instance=task)  #editing existing element
        
        if form.is_valid():
            form.save(commit=False).manage = Response.user
            form.save()
            
            messages.success(Response,"task successfully edited!")
        return redirect('todolist')
    else:
        
        task = tasklist.objects.get(pk=task_id)
        if task.manage == Response.user:
            return render(Response,'edit.html',{'task':task}) 
        else:
            return redirect('home')          

@login_required
def todolist(Response):
    
    if Response.method == "POST":
        #form = taskform(Response.POST or None) #adding new element
        task= Response.POST.get('task',False)
        manage=Response.user
        priority = Response.POST.get('priority',False)
        done =False
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()
        current_date = today.strftime("%Y-%m-%d")
        start_on = current_date
        start_at = current_time                   
        form = tasklist.objects.create(manage=manage, task=task,priority= priority ,start_at=start_at,start_on=start_on,done=done)
        form.save()
        messages.success(Response,"task succesffuly added!")
        return redirect('todolist')
        
    else:
        #print(Response.user)
        #rows=tasklist.objects.raw('SELECT id,start_on,SUM(point) FROM todolist_app_tasklist WHERE manage="abv" and done=1 GROUP BY start_on'),
        acc=str(Response.user)
        #rows=tasklist.objects.raw('SELECT todolist_app_tasklist.id,start_on,SUM(point) FROM auth_user INNER JOIN todolist_app_tasklist ON auth_user.id = todolist_app_tasklist.manage_id WHERE username=%s and done=1 GROUP BY start_on',[acc])
        #for row in rows:
            #print(row["SUM(point)"])
        #print(Response.user)
        #for row in rows:
            #print(row)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()
        current_date = today.strftime("%Y-%m-%d")
        start_on = current_date
        start_at = current_time          
        all_task = tasklist.objects.filter(manage=Response.user)
        paginator = Paginator(all_task,10)
        page = Response.GET.get('pg')
        all_task = paginator.get_page(page)

        #rows=tasklist.objects.raw('SELECT * FROM todolist_app_tasklist')
        connection = sqlite3.connect("db.sqlite3")
        crsr = connection.cursor() 
        crsr.execute('''SELECT todolist_app_tasklist.id,start_on,SUM(point) FROM auth_user INNER JOIN todolist_app_tasklist ON auth_user.id = todolist_app_tasklist.manage_id WHERE username=? and done=1 and start_on=? GROUP BY start_on''',(acc,start_on))
        rows=crsr.fetchall()
        connection.commit()
        connection.close()         
        return render(Response,'todolist.html',{'all_task':all_task,"rows":rows})

def contactus(Response):
    return render(Response,'contactus.html') 

def aboutus(Response):
    return render(Response,'aboutus.html')       

