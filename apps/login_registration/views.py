from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import *
import bcrypt

def index(request):
    return render(request, 'login_registration/index.html')

def welcome(request):
    # check if session id exist
    if 'user_id' not in request.session:
        messages.error(request, 'You need be to logged in to see this page!', 'logout')
        return redirect('/')
    
    user = User.objects.values().get(id = request.session['user_id'])
    return render(request, 'login_registration/welcome.html', user)


def login(request):
    if request.method != 'POST':
        messages.error(request, '*You must logged in first', 'login')
        return redirect('/')
    
    # no validation error so fetch the user data
    user = User.objects.filter(email = request.POST['email'])
    if not user: # if the user email doesn't exist redirect it back with error
        messages.error(request, '*Email or password is invalid', 'login')
        return redirect('/')

    user = user[0] # since it is a list, get the first element
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        # password match so loggedthe user in 
        request.session['user_id'] = user.id
        return redirect('/welcome')
    else:
        # password did not match so redirect the user back to fix the error
        messages.error(request, '*Email or password is invalid', 'login')
        return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')


def register(request):
    # if it is not a post request return to the home page
    if request.method != "POST":
        return redirect('/')

    errors = User.objects.basic_validator(request.POST)
    # check if any errors exist
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, key)

            # record form data to sessions
            request.session['first_name'] = request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['email'] = request.POST['email']
            request.session['birthday'] = request.POST['birthday']
            request.session['city'] = request.POST['city']
            request.session['state'] = request.POST['state']
            request.session['zipcode'] = request.POST['zipcode']
        return redirect('/')
    else:
        # check email already exist in the database
        user = User.objects.filter(email = request.POST['email'])
        if user:
            messages.error(request, '*Email already exist', 'email')
            request.session['first_name'] = request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['email'] = request.POST['email']
            request.session['birthday'] = request.POST['birthday']
            request.session['city'] = request.POST['city']
            request.session['state'] = request.POST['state']
            request.session['zipcode'] = request.POST['zipcode']
            return redirect('/')

        # Hash the user password first
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects # create an object of the user table
        user.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            birthday = request.POST['birthday'],
            city = request.POST['city'],
            state = request.POST['state'],
            zipcode = request.POST['state'],
            password = hash_pw
        )

    request.session.clear()
    request.session['user_id'] = user.last().id
    return redirect('/welcome')

