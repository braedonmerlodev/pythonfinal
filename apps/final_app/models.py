from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt
from datetime import date

NAME_REGEX = re.compile(r'^[A-Za-z ]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = []
        if len(postData["password"]) < 8:
            errors.append("Password must be greater than 8 characters!")
        elif postData["pw_confirm"] != postData["password"]:
            errors.append("Passwords did not match!")
        if not re.match(NAME_REGEX, postData['name']) or not re.match(NAME_REGEX, postData['alias']):
            errors.append("First & Last name fields must only contain letters")
        if not re.match(EMAIL_REGEX, postData['email']):
            errors.append("Email is not valid")
        if len(postData["name"]) < 2:
            errors.append("First Name field must not be longer than 2 characters!")
        if len(postData["alias"]) < 2:
            errors.append("Last Name field must not be longer than 2 characters!")
        if len(postData["birthday"]) < 1:
            errors.append("You must submit a birthday!")
        if not errors:
            if self.filter(email = postData["email"]):
                    errors.append("Email already registered")
            else:
                hashed = bcrypt.hashpw((postData['password']. encode()), bcrypt.gensalt(5))
                newUser = self.create(
                    name = postData['name'],
                    alias = postData['alias'],
                    email = postData['email'],
                    birthday = postData['birthday'],
                    password = hashed
                )
        return errors

    def login_validator(self, postData):
        errors = []

        users = self.filter(email = postData["email"])
        if users:
            user = users[0]
            if bcrypt.checkpw(postData["password"].encode(), user.password.encode()):
                return user

        errors.append('email/password not in records!')
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {} {} {}>".format(self.name, self.alias, self.email, self.birthday, self.password)


class Poke(models.Model):
    users = models.ManyToManyField(User, related_name = "pokes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
