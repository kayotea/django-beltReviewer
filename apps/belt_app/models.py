# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime

NAME_REGEX = re.compile(r'^[a-zA-Z]{2,50}$')
ALIAS_REGEX = re.compile(r'[a-zA-Z0-9.+_-]{2,50}')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PWD_REGEX = re.compile(r'^.{8,50}$')

#validate user inputs for review

# Create your models here.
class UserManager(models.Manager):
    def validate_me(self, postData):
        error = []
        #get info from postData: readability
        name = postData['name']
        alias = postData['alias']
        email = postData['email']
        pwd = postData['password']
        c_pwd = postData['confirm_password']

        #validations
        if not NAME_REGEX.match(name):
            error.append('Name is invalid.')
        if not ALIAS_REGEX.match(alias):
            error.append('Alias is invalid.')
        if not EMAIL_REGEX.match(email):
            error.append('Email is invalid.')
        if not PWD_REGEX.match(pwd):
            error.append('Password too short')
        if pwd != c_pwd:
            error.append('Passwords do not match')
        
        #check that given email is not already stored
        num_emails = User.objects.filter(email=email).count()
        #check that given alias is not already being used
        num_alias = User.objects.filter(alias=alias).count()
        if num_emails != 0:
            error.append('User with that email already exists')
        if num_alias != 0:
            error.append('That alias is already in use')
        
        #if no erros, add user
        if len(error) == 0:
            pwd = pwd.encode('utf-8')
            hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
            user = User.objects.create(name=name, alias=alias, email=email, password=hashed_pwd)
            return [True, user]
        #if there are errors, don't add user
        else:
            return [False, error]
    def login_user(self, postData):
        #get info from postData: readability
        eml = postData['email']
        pwd = postData['password'].encode('utf-8')
        #look for match in registered users
        users = User.objects.all()
        for user in users:
            user.password = user.password.encode('utf-8')
            if eml == user.email and bcrypt.hashpw(pwd, user.password) == user.password:
                return [True, user.id]
        return [False, False]

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __unicode__(self):
        return 'id: '+str(self.id)

class AuthorManager(models.Manager):
    def author_check(self, author):
        author_exists = Author.objects.filter(name=author)
        if author_exists:
            author_exists = Author.objects.get(name=author)
            print "author exists:",author_exists
            return author_exists
        else:
            new_author = Author.objects.create(name=author)
            print "new author:",new_author
            return new_author

class Author(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AuthorManager()

    def __unicode__(self):
        return 'author: '+str(self.id)+" name:"+self.name

class BookManager(models.Manager):
    def add_book(self, postData):
        title = postData['title']
        author = postData['author']
        book = Book.objects.filter(title=title, author=author)
        #if no book of matching title and author was found
        if not book:
            book = Book.objects.create(title=title, author=author)
            print "no book was found, new book created:",book
        else:
            book = Book.objects.get(title=title, author=author)
        return book


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()

    def __unicode__(self):
        return 'book: '+str(self.id)+"title:"+self.title

class ReviewManager(models.Manager):
    def add_review(self, postData):
        book = postData['book']
        user = postData['user']
        review = postData['review']
        rating = postData['rating']

        new_review = Review.objects.create(book=book, user=user, review=review, rating=rating)
        print "new review:",new_review
        return

class Review(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    review = models.TextField(max_length=1000)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()

    def __unicode__(self):
        return 'review: '+str(self.id)+' , book:'+str(self.book.title)+' , user: '+str(self.user.name)