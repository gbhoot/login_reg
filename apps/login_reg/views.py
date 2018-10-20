from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import datetime
import bcrypt

# Create your views here.
def index(request):
    if 'id' in request.session:
        return redirect('/profile')
    return render(request, 'index.html')

def processRegister(request):
    if 'id' in request.session:
        return redirect('/profile')
    
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

    return redirect('/profile')

def processLogin(request):
    if 'id' in request.session:
        return redirect('/profile')
    
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    
    user = User.objects.get(email=request.POST['emailL'])
    
    request.session['id'] = user.id

    return redirect('/profile')

def profile(request):
    if 'id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['id'])
    data = {
        'user'  :   user,
    }

    return render(request, 'profile.html', data)

def logout(request):
    if 'id' not in request.session:
        return redirect('/')
    
    request.session.clear()

    return redirect('/')