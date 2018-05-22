from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def landing(request):
	if 'loggedIn' not in request.session:
		request.session['loggedIn'] = False
		return redirect('users/login')
	if request.session['loggedIn'] == True:
		return render(request, 'Users/User.html')
	else:
		return redirect('users/login')

def login(request):
	return render(request, 'Users/login.html')


def logout(request):
	request.session.clear()
	return redirect('/users')


def createUser(request):
	errors = User.objects.UserVal(request.POST)
	if len(errors) > 0:
		request.session['first_name'] = request.POST['first_name']
		request.session['last_name'] = request.POST['last_name']
		request.session['email'] = request.POST['email']
		for key,value in errors.items():
			messages.error(request, value)
		return redirect('/users')
	else:
		first_name = request.POST['first_name'].strip()
		last_name = request.POST['last_name'].strip()
		email = request.POST['email'].strip()
		pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		U = User.objects.create(first_name=first_name, last_name=last_name, email = email, password_hash = pw_hash)
		U.save()
		request.session['first_name'] = U.first_name
		request.session['last_name'] = U.last_name
		request.session['loggedIn'] = True
		print("\n\n user created \n\n")
		return redirect('/users')

def loginUser(request):
	errors = User.objects.loginVal(request.POST)
	if errors:
		for key,value in errors.items():
			messages.error(request, value)
		return redirect('/users')
	else:
		email = request.POST['email']
		U = User.objects.get(email = email)
		request.session['first_name'] = U.first_name
		request.session['last_name'] = U.last_name
		request.session['loggedIn'] = True
		return redirect('/users')




