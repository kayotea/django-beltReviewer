# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User, Author, Book, Review


# Create your views here.
def index(request):
    return render(request, 'belt_app/index.html')

def register(request):
    if request.method == "POST":
        #get user inputs
        postData = {
            'name' : request.POST['name'],
            'alias' : request.POST['alias'],
            'email' : request.POST['email'],
            'password' : request.POST['password'],
            'confirm_password' : request.POST['confirm_password']
        }
        #validate inputs. if valid, crate user
        user = User.objects.validate_me(postData)
        #if user created
        if user[0] == True:
            request.session['login'] = user[1].id
            return redirect('/books')
        #if user was not created
        else:
            errors = user[1]
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/')

def login(request):
    #get user inputs
    if request.method == "POST":
        postData = {
            'email' : request.POST['email'],
            'password' : request.POST['password']
        }
    #check for match in stored useres & login
    user = User.objects.login_user(postData)
    #if login successful
    if user[0]:
        request.session['login'] = user[1]
        return redirect('/books')
    else:
        messages.add_message(request, messages.INFO, 'Invalid login')
        return redirect('/')

def recent_reviews(request):
    recent_three_reviews = Review.objects.all().order_by('-created_at')[:3]
    context = {
        'user' : User.objects.get(pk=request.session['login']),
        'reviews' : recent_three_reviews,
        'books' : Book.objects.all()
    }
    return render(request, 'belt_app/books.html', context)

def add_book_review(request):
    context = {
        'authors' : Author.objects.all().order_by('name')
    }
    return render(request, 'belt_app/add_book.html', context)

def add_book_process(request):
    if request.method == "POST":
        title = request.POST.get('title', False)       #book title
        author1 = request.POST['author1']   #author by author id
        author2 = request.POST['author2']   #new author by name (string)
        review = request.POST['review']     #review text
        stars = request.POST['stars']       #number of stars
        print "title:",title
        print "author1:",author1
        print "author2:",author2
        print "review:",review
        print "stars:",stars
        #get an author:
        #if user inputted a new author, check if author already exists.
        #if author exists, returns that author
        #if author doesn't exist, create author and return it
        if len(author2):
            author = Author.objects.author_check(author2)   #get author object
            print "author2"
        #if user has not inputted a new author
        else:
            author = Author.objects.get(pk=author1)         #get author object
            print "author1"

        #check if book title already exists, if not, add book
        postData = {
            'title' : title,
            'author' : author
        }
        book = Book.objects.add_book(postData)  #get book object
        print "book:",book

        #add review for book
        postData = {
            'book' : book,
            'user' : User.objects.get(pk=request.session['login']),
            'review' : review,
            'rating' : stars
        }
        Review.objects.add_review(postData)
    return redirect('/books/{}'.format(book.id))

def book_reviews(request, id):
    #get given book
    book = Book.objects.get(pk=id)
    #get reviews for given book
    reviews_for_book = Review.objects.filter(book=book)
    print reviews_for_book
    context = {
        'user' : User.objects.get(pk=request.session['login']),
        'book' : book,
        'reviews' : reviews_for_book
    }
    return render(request, 'belt_app/show_book.html', context)

def delete_review(request, id):
    review = Review.objects.get(pk=id)
    book_id = review.book.id
    review.delete()
    return redirect('/books/{}'.format(book_id))

def review_book(request, id):
    if request.method == "POST":
        #add review for book
        postData = {
            'book' : Book.objects.get(pk=id),
            'user' : User.objects.get(pk=request.session['login']),
            'review' : request.POST['review'],
            'rating' : request.POST['stars']
        }
        Review.objects.add_review(postData)
    return redirect('/books/{}'.format(id))

def show_user(request, id):
    #get user
    user = User.objects.get(pk=id)
    #get reviews by user
    reviews = Review.objects.filter(user=user)
    review_count = reviews.count()
    context = {
        'user' : user,
        'reviews' : reviews,
        'review_count' : review_count
    }
    print reviews
    print review_count
    return render(request, 'belt_app/show_user.html', context)

def logout(request):
    del request.session['login']
    request.session.modified = True
    return redirect('/')