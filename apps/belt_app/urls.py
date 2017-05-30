from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/process$', views.register),
    url(r'^login$', views.login),
    url(r'^books/add$', views.add_book_review, name='add_review'),
    url(r'^books/add/process$', views.add_book_process),
    url(r'^books/(?P<id>\d+)$', views.book_reviews, name='show_book'),
    url(r'^delete/review/(?P<id>\d+)$', views.delete_review),
    url(r'^books/review/(?P<id>\d+)$', views.review_book),
    url(r'^books/$', views.recent_reviews, name='home'),
    url(r'^users/(?P<id>\d+)$', views.show_user),
    url(r'^logout$', views.logout, name='logout')
]