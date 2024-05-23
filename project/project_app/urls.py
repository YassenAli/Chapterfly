from django.urls import path
from . import views

urlpatterns = [
    path('',views.main, name='index'),
    path('cart/', views.cart, name='cart'),
    path('view/', views.view, name='view'),
    path('details/<str:id>/', views.details, name='details'),
    path('add_book/', views.add_book, name='add_book'),
    path('account/', views.account, name='account'),
    path('LoginSignup/', views.LoginSignup, name='LoginSignup'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('add_love/', views.add_love, name='add_love'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
]
