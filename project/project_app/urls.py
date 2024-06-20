from django.urls import path
from . import views

urlpatterns = [
    path('',views.main, name='index'),
    path('cart/', views.cart, name='cart'),
    path('view/', views.view, name='view'),
    path('details/<str:id>/', views.details, name='details'),
    path('view/add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add_book/', views.add_book, name='add_book'),
    path('account/', views.account, name='account'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('add_love/', views.add_love, name='add_love'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('logout/', views.logout, name='logout'),
    path('get_profile_picture/', views.get_profile_picture_ajax, name='get_profile_picture'),
    path('update_profile_photo_ajax/', views.update_profile_photo_ajax, name='update_profile_photo_ajax'),
    path('navbarAdmin/', views.navbarAdmin ,name='navbarAdmin' ),
    path('status/details/', views.status_details, name='status_details'),
    path('status/views/', views.status_views, name='status_views'),
    path('LoginSignup/', views.render_login_signup_page, name='LoginSignup'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login,name='login'),

]
