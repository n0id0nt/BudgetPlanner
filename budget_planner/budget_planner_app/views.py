from datetime import datetime
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from .forms import PostForm, ItemForm, PredictionForm
from .models import Post, Report, Item, Prediction
from django.db.models import Count

def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()

    posts = Post.objects.filter(hidden=False).order_by('-date_posted').all()
    
    context = {'form' : form, 'posts': posts}

    return render(request, 'budget_planner_app/index.html', context)

def delete_post(request, post_id):
    # check if post belongs to user
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        post.delete()
    #remove it from the database
    #redirect back to the same page
    return redirect('index')

@login_required
def logout(request):
    django_logout(request)
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = 'http://127.0.0.1:8000'
    return redirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')

@permission_required('budget_planner_app.view_report', raise_exception=True)
def reports(request):
    reports = Post.objects.annotate(times_reported=Count('report')).filter(times_reported__gt=0).all()

    context = {'reports' : reports}

    return render(request, 'budget_planner_app/reports.html', context)

def report_post(request, post_id):
    post = Post.objects.get(id=post_id)

    report, created = Report.objects.get_or_create(reported_by=request.user, post=post) # getorcreate stops user from creating multiple reports

    if created:
        report.save()

    return redirect('index')

@permission_required('budget_planner_app.change_post', raise_exception=True)
def hide_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.hidden = True
    post.date_hidden = datetime.now()
    post.hidden_by = request.user
    post.save()
    return redirect('reports')

@permission_required('budget_planner_app.change_user')
def block_user(request, user_id):
    User = get_user_model()

    user = User.objects.get(id=user_id)
    for post in user.post_set.all():
        if not post.hidden:
            post.hidden = True
            post.hidden_by = request.user
            post.date_hidden = datetime.now()
            post.save()

    user.is_active = False
    user.save()

    return redirect('reports')

# budget planner methods
@login_required
def budget(request):

    item_form = ItemForm()

    # get all the items in the budget
    items = Item.objects.filter(user=request.user)

    values = []

    for item in items:
        prediction_form = PredictionForm()
        prediction_form.fields['item'].initial = item
        # check that prediction exists for item
        if Prediction.objects.filter(item=item).exists():
            prediction_form.fields['amount'].initial = Prediction.objects.get(item=item).amount
        else:
            prediction_form.fields['amount'].initial = Decimal(0).quantize(Decimal('0.00'))

        values.append({'item': item, 'prediction_form': prediction_form})

    context = {'item_create_form' : item_form, 'values' : values}

    return render(request, 'budget_planner_app/budget.html', context)

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()

    return redirect('budget')

def delete_item(request, item_id):
    # check if item belongs to user
    item = Item.objects.get(id=item_id)
    if item.user == request.user:
        item.delete()
    #remove it from the database
    #redirect back to the same page
    return redirect('budget')

def create_prediction(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            # check if prediction belongs to item
            item = Item.objects.get(id=form.cleaned_data['item'].id)
            # check if item belongs to user
            if item.user == request.user:
                prediction, created = Prediction.objects.update_or_create(item=item, defaults=form.cleaned_data) # getorcreate stops user from creating multiple reports

                if created:
                    prediction.save()

    return redirect('budget')

def create_actual_item_amount(request):
    pass