from django.shortcuts import render,redirect
from . models import Task
from . forms import Todoforms
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy
# Create your views here.

class TaskListView(ListView):
    model=Task
    template_name= "taskview.html"
    context_object_name= "result"  #result-> taskview-result

class TaskDetailView(DetailView):
    model=Task
    template_name= "detail.html"
    context_object_name="i"  #i-> taskview-loopvar i

class TaskUpdateView(UpdateView):
    model = Task
    template_name = "update.html"
    context_object_name = "task" #just name
    fields = ('name','priority','date')
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "remove.html"
    success_url=reverse_lazy("cbvtask")#name in taskview url


def taskview(request):
    ob=Task.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        priority=request.POST.get("priority")
        date = request.POST.get("date")
        obj=Task(name=name,priority=priority,date=date)
        obj.save()
    return render(request,"taskview.html",{"result":ob})

# def task(request):
#
#     return render(request,"task.html")
def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method=="POST":
        task.delete()
        return redirect('/')
    return render(request,'delete.html',{'task':task})

def update(request,tid):
    try:
        task1=Task.objects.get(id=tid)
        form=Todoforms(request.POST or None,instance=task1)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request,'edit.html',{'task':task1,'form':form})
    except:
        import traceback
        traceback.print_exc()