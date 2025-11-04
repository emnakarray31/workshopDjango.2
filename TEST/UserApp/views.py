from django.shortcuts import render,redirect
from .forms import registerUserForm
# Create your views here.
def register(req):
    if req.method == "POST":
        form = registerUserForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("Login")
        else:
            form = registerUserForm()
            return render(req, 'register.html',{"form":form})
        return render(req, 'register.html',{"form":form})


