from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import BookForm, CategoryForm, CheckoutForm, EditBookForm , SignupForm

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

def details(request, id):
    bookID = Book.objects.get(id=id)
    context = {
        'book': bookID
    }
    return render(request, 'pages/details.html', context)


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

def LoginSignup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SignupForm()
    return render(request , 'pages/LoginSignup.html' , {'SignupForm' : form})


 