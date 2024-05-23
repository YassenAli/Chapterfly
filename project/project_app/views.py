from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import BookForm, CategoryForm, CheckoutForm, EditBookForm , SignupForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.

def view(request):
    search = Book.objects.all()
    title = None
    if 'search-name' in request.GET:
        title = request.GET['search-name']
        if title:
            search = search.filter(name__icontains=title)
        
    context = {
        'category': Category.objects.all(),
        'books': search,
    }
    return render(request, 'pages/views.html', context)


def add_book(request):
    if request.method == 'POST':
        if 'add_book' in request.POST:
            add_book = BookForm(request.POST, request.FILES) # request.FILES  to save images
            if add_book.is_valid():
                add_book.save()

        elif 'add_category' in request.POST:
            add_category = CategoryForm(request.POST)
            if add_category.is_valid():
                add_category.save()
        
    context = {
        'form': BookForm(),
        'formCategory': CategoryForm(),
    }
    return render(request, 'pages/add_book.html', context)

def cart(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            return redirect('account')
    context = {
        'form': CheckoutForm(),
    }
    return render(request, 'pages/cart.html', context)

def main(request):
    return render(request, 'pages/main.html')

def account(request):
    #get username
    #get profile picture
    context = { #will be updated after setting a model for acc data
        # 'name' : 'default'
        #'username' : username
        #'profilepic' : profilepic
    }
    return render(request, 'pages/accountUser.html', context)

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = EditBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('view')  
    else:
        form = EditBookForm(instance=book)
    return render(request, 'pages/edit_book.html', {'form': form})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('view')
    return render(request, 'pages/delete_book.html', {'book': book})

# def details(request, id):
#     bookID = Book.objects.get(id=id)
#     context = {
#         'book': bookID
#     }
#     if request.method == 'POST' and 'add-to-wishlist' in request.POST:
#         profile = Profile.objects.get(user=request.user)
#         profile.wishlist.add(bookID)
#         return JsonResponse({'status': 'success'})
#     return render(request, 'pages/details.html', context)

# def add_love(request):
#     if request.method == 'POST':
#         book_id = request.POST.get('book-id')
#         book = Book.objects.get(id=book_id)
#         profile = Profile.objects.get(user=request.user)
#         # profile = request.user.profile
#         if book in profile.wishlist.all():
#             return JsonResponse({'status': 'already_in_wishlist'})
#         else:
#             profile.wishlist.add(book)
#             return JsonResponse({'status': 'success'})
#     return HttpResponseBadRequest() 

@login_required
def details(request, id):
    try:
        bookID = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponseBadRequest('Book does not exist')

    if request.method == 'POST' and 'add-to-wishlist' in request.POST:
        profile = Profile.objects.get(user=request.user)
        profile.wishlist.add(bookID)
        return JsonResponse({'status': 'success'})

    context = {
        'book': bookID
    }
    return render(request, 'pages/details.html', context)

@csrf_exempt
def add_love(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('LoginSignup')

        book_id = request.POST.get('book-id')
        try:
            book = Book.objects.get(id=book_id)
            profile = Profile.objects.get(user=request.user)
        except (Book.DoesNotExist, Profile.DoesNotExist):
            return HttpResponseBadRequest('Book or user does not exist')

        if book in profile.wishlist.all():
            return JsonResponse({'status': 'already_in_wishlist'})
        else:
            profile.wishlist.add(book)
            return JsonResponse({'status': 'success'})

    return HttpResponseBadRequest()

def wishlist(request):
    context = {
        'books': Profile.objects.get(user=request.user).wishlist.all(),
    }
    return render(request, 'pages/add_love.html', context)
    
def LoginSignup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SignupForm()
    return render(request , 'pages/LoginSignup.html' , {'SignupForm' : form})


def get_profile_picture(username):
    user = Signup.objects.get(username=username)
    profile_picture_url = user.profilePicture.url
    return profile_picture_url


def borrow_book(book_id):
    book = get_object_or_404(Book, pk=book_id)

    if book.status == 'available':
        book.status = 'borrowed'
        book.save()
        return ('Book successfully borrowed') #update to make it a json response
    else:
        return ('Book is not available for borrowing') #update to make it a json response


