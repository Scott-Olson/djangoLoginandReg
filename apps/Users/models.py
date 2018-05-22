from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import bcrypt
import re


def newPasswordValidator(pw):
	result = True
	upper = 0
	lower = 0
	number = 0
	nonAlphaNum = 0
	for char in pw:
		if char.isupper():
			upper += 1
		if char.islower():
			lower += 1
		if char.isnumeric():
			number += 1
		if not char.isspace() and not char.isalnum():
			nonAlphaNum += 1
	if upper == 0 or lower == 0 or number == 0 or nonAlphaNum == 0:
		result = False
	print(result, upper, lower, number, nonAlphaNum)
	return result

r = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
def isEmailValid(email):
	if len(email) > 7:
		if re.match(r, email) != None:
			return True

# Create your models here.
class BasicVal(models.Manager):
	def UserVal(self, postData):
		print("in here")
		errors={}
		first_name = postData['first_name'].strip()
		last_name = postData['last_name'].strip()
		email = postData['email'].strip()
		try:
			User.objects.get(email = email)
			print('email exists already')
			errors['email'] = "Enter a valid email address"
		except:
			print('exist email val')
		print('this far 4')
		validEmail = isEmailValid(email)
		if not validEmail:
			errors['email'] = "Enter a valid email address"
		if len(first_name) < 2:
			errors['first_name'] = "First name too short"
		if not first_name.isalpha():
			errors['first_name2'] = "Only letters accepted in first name"
		if len(last_name) < 2:
			errors['last_name'] = "Last name too short"
		if not last_name.isalpha():
			errors['last_name2'] = "Only letters accepted in last name"
		if len(postData['password'])<8:
			errors['password1'] = "Password too short, must be 8 characters"
		pwValid = newPasswordValidator(postData['password'])
		if pwValid == False:
			errors['password2'] = "Password must contain at least one capital letter, one special character, and one number."
		if postData['password'] != postData['password_conf']:
			errors['password3'] = "Passwords don't match"
		print(errors)
		return errors

	def loginVal(self, postData):
		email = postData['email'].strip()
		pw = postData['password']
		errors={}
		U = User.objects.filter(email = email).first()
		if email:
			print("\n INHERE \n")
			if not U:
				errors['email'] = "invalid email"
				return errors
			if bcrypt.checkpw(pw.encode(), U.password_hash.encode()):
				return
			else:
				errors['password'] = "incorrect password"	
		else:
			errors['login'] = "invalid login"
		return errors

class User(models.Model):
	first_name = models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password_hash = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = BasicVal()
	def __repr__(self):
		return "<User Object: {} , {}>".format(self.first_name, self.last_name)




