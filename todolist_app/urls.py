from django.urls import path
from todolist_app import views

urlpatterns = [
    path('',views.todolist,name = 'todolist'),
    path('comppend/<task_id>',views.comppend,name = 'comp_pend'),
    path('deletetask/<task_id>',views.deletetask,name = 'delete_task'),
    path('edittask/<task_id>',views.edittask,name = 'edit_task'),
   
  
]
