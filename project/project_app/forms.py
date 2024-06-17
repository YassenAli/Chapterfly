from django import forms
from .models import Book, Category, Checkout , Signup


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        widgets = {
            'category': forms.Select(),
            'status': forms.Select(),
            'price': forms.NumberInput(),
            'id': forms.NumberInput(),
            'img': forms.FileInput(),
            # 'img': forms.FilePathField(),
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = [
            'cardholder_name',
            'card_number',
            'expiration_date',
            'cvv'
        ]
        widgets = {
            'cardholder_name': forms.TextInput(attrs={'size': '17', 'type': 'text', 'class': 'form-control form-control-lg', 'placeholder': "Cardholder's Name", 'id': 'typeName'}),
            'card_number': forms.NumberInput(attrs={'maxlength': '17', 'minlength': '17', 'size': '17', 'type': 'text', 'class': 'form-control form-control-lg', 'placeholder': '1234 5678 9012 3457', 'id': 'typeTextCardnum'}),
            # 'card_type': forms.Select(),
            'expiration_date': forms.DateInput(attrs={'maxlength': '7', 'minlength': '7', 'size': '7', 'type': 'text', 'class': 'form-control form-control-lg', 'placeholder': 'MM/YYYY', 'id': 'typeExp'}),
            'cvv': forms.NumberInput(attrs={'maxlength': '3', 'minlength': '3', 'size': '1', 'type': 'password', 'class': 'form-control form-control-lg typeText', 'placeholder': '●●●', 'id': 'typeText'}),
        }

class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['description', 'name', 'author', 'price', 'category', 'status']

class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['username', 'email', 'password' ,'confirmPassword', 'isAdmin' , ]
        labels = {
            'username': '',
            'email': '',
            'password': '',
            'confirmPassword': '',
            'isAdmin': 'Sign up as Admin',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': ' username', 'class': 'form_field'}),
            'email': forms.EmailInput(attrs={'placeholder': ' email', 'class': 'form_field'}),
            'password': forms.PasswordInput(attrs={'placeholder': ' password', 'class': 'form_field'}),
            'confirmPassword': forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'form_field'}),
            'isAdmin': forms.CheckboxInput(),

        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Signup.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Signup.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_confirmPassword(self):
        password = self.cleaned_data.get('password')
        confirmPassword = self.cleaned_data.get('confirmPassword')
        if password and confirmPassword and password != confirmPassword:
            raise forms.ValidationError("Passwords do not match")
        return confirmPassword      

class loginForm(forms.Form):
    usernameLogin = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form_field'}),
        label=''
    )
    passwordLogin = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form_field'}),
        label=''
    )

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['profilePicture']
