from django.shortcuts import render, redirect, HttpResponse


def landing(request):
	response = "Click <a href='/users'>here</a> to go to the login page"
	return HttpResponse(response)