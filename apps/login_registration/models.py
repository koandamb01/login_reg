from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
ZIPCODE_REGEX = re.compile(r'^([0-9]){5}(([ ]|[-])?([0-9]){4})?$')
WORD_SPACE_REGEX = re.compile(r'^[A-Za-z ]+')

class UserManager(models.Manager):
    def basic_validator(slef, postData):
        errors = {}
        # validation for firstname
        if len(postData['first_name']) == 0:
            errors['first_name'] = "*First Name is required"
        elif len(postData['first_name']) < 3:
            errors['first_name'] = "*Must be more than 2 characters"
        elif not postData['first_name'].isalpha():
            errors['first_name'] = "*Alphabets characters only"
        
        # validation for lastname
        if len(postData['last_name']) == 0:
            errors['last_name'] = "*Last Name is required"
        elif len(postData['last_name']) < 3:
            errors['last_name'] = "*Must be more than 2 characters"
        elif not postData['last_name'].isalpha():
            errors['last_name'] = "*Alphabets characters only"
        
        # validation for email
        if len(postData['email']) == 0:
            errors['email'] = "*Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "*Invalid email"

        # validation for birthday
        if len(postData['birthday']) == 0:
            errors['birthday'] = "*Birthday is required"
        else:
            this_year = datetime
            mydate = datetime.strptime("2008-01-01", "%Y-%m-%d")
            birth_year = datetime.strptime(postData['birthday'], '%Y-%m-%d')

            #check if birthday is in range
            if mydate < birth_year:
                errors['birthday'] = "*You are not enough to register"
        
        # validation for city
        if len(postData['city']) == 0:
            errors['city'] = "*City is required"
        elif not WORD_SPACE_REGEX.match(postData['city']):
            errors['city'] = "*Alphabets characters only"

        # validation for state
        if len(postData['state']) == 0:
            errors['state'] = "*State is required"

        # validation for zipcode
        if len(postData['zipcode']) == 0:
            errors['zipcode'] = "*Zipcode is required"
        elif not ZIPCODE_REGEX.match(postData['zipcode']):
            errors['zipcode'] = "*Invalid zipcode"

        # validation for password
        if len(postData['password']) == 0:
            errors['password'] = "*Password is required"
        elif len(postData['password']) < 8:
            errors['password'] = '*Password must be at least 8 characters'
        elif not re.search('[0-9]', postData['password']):
            errors['password'] = '*Password must have at leat one number'
        elif not re.search('[A-Z]', postData['password']):
            errors['password'] = '*Password must have at least one Caplital letter'
        elif postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = '*Password must be match'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    birthday = models.DateField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()