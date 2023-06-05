from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'budget_planner_app/index.html')

def reports(request):
    return render(request, 'budget_planner_app/reports.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'Post':
        form = UserCreationForm(request.Post)
        if form.is_valod():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'budget_planner_app/signup.html', {form:form})
    else:
        form = UserCreationForm()
        return render(request, 'budget_planner_app/signup.html', {form:form})
    
def signin(request):
    if request.user.is_authenticated:
        render(request, 'budget_planner_app/index.html')
    if request.method == 'Post':
        username = request.POST('username')
        password = request.POST('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'budget_planner_app/signip.html', {form:form})
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect('/')