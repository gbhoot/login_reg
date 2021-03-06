from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote, Like
from django.utils import timezone, timesince
import pytz
import datetime
import bcrypt
from django import template
register = template.Library()

# Create your views here.
def index(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    return render(request, 'index.html')

def processRegister(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    
    print("errors are coming")
    errors = User.objects.reg_validator(request.POST)
    
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
            
    currentTime = datetime.datetime.now()
    
    # Hash password and prepare for registration
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    newUser = User.objects.create(first_name=request.POST['fName'], last_name=request.POST['lName'], 
        email=request.POST['email'], password=pw_hash, created_at = currentTime, updated_at = currentTime)
    request.session['id'] = newUser.id

    return redirect('/dashboard')

def processLogin(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    
    user = User.objects.get(email=request.POST['emailL'])
    
    request.session['id'] = user.id

    return redirect('/dashboard')

@register.filter
def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')

    

    user = User.objects.get(id=request.session['id'])
    likes = Like.objects.all()

    # for like in likes:
    #     like.delete()

    data = {
        'user'      :   user,
        'quotes'    :   Quote.objects.order_by("-created_at"),
        'like'      :   [False],
        'likes'     :   [0],
    }

    if likes:
        for quote in data['quotes']:
            data['likes'].append(int(Like.objects.count_likes(quote)))
            error = Like.objects.like_validator(quote, user)
            if len(error):
                data['like'].append(True)
            else:
                data['like'].append(False)

    print(data['like'])
    print(data['likes'])
    
    return render(request, 'dashboard.html', data)

def profile(request):
    if 'id' not in request.session:
        return redirect('/')
    
    data = {
        'user'      :   User.objects.get(id=request.session['id']),
    }

    return render(request, 'profile.html', data)

def show(request, id):
    if 'id' not in request.session:
        return redirect('/')

    quoter = User.objects.get(id=id)
    
    data = {
        'user'      :   User.objects.get(id=request.session['id']),
        'quoter'    :   quoter,
        'quotes'    :   Quote.objects.filter(user=quoter).order_by("-created_at"),
    }

    return render(request, 'quoter.html', data)

def update(request):
    if 'id' not in request.session:
        return redirect('/')

    errors = User.objects.reg_validator(request.POST, request.session['id'], True)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/account')

    user = User.objects.get(id=request.session['id'])
    
    user.first_name = request.POST['fName']
    user.last_name = request.POST['lName']
    user.email = request.POST['email']
    user.updated_at = datetime.datetime.now()
    user.save()

    return redirect('/account')


def addQuote(request):
    if 'id' not in request.session:
        return redirect('/')
    
    errors = Quote.objects.quote_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    
    currentT = timezone.now()
    user = User.objects.get(id=request.session['id'])
    newQuote = Quote.objects.create(author=request.POST['author'], content=request.POST['content'], 
        created_at=currentT, updated_at=currentT, user=user)
    
    print("Successfully added: ", newQuote)
    
    return redirect('/dashboard')

def deleteQuote(request, id):
    if 'id' not in request.session:
        return redirect('/')
    
    quote = Quote.objects.get(id=id)
    quote.delete()

    return redirect('/dashboard')

def likeQuote(request, id):
    if 'id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['id'])
    quote = Quote.objects.get(id=id)
    currentTime = timezone.now()

    error = Like.objects.like_validator(quote, user)
    if len(error):
        return redirect('/dashboard')

    newLike = Like.objects.create(user=user, quote=quote, created_at=currentTime, updated_at=currentTime)

    print(newLike)

    return redirect('/dashboard')
    
def logout(request):
    if 'id' not in request.session:
        return redirect('/')
    
    request.session.clear()

    return redirect('/')