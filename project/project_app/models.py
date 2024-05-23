from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Checkout(models.Model):
    CARD_TYPE_CHOICES = [
        ('Visa', 'Visa'),
        ('MasterCard', 'MasterCard'),
        ('amex', 'amex'),
        ('payPal', 'payPal')
    ]
    cardholder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=19)
    card_type = models.CharField(max_length=10, choices=CARD_TYPE_CHOICES)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return self.cardholder_name
    
    class Meta:
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'
        ordering = ['cardholder_name']
      
class Book(models.Model):
    status_book = [
        ('available', 'available'),
        ('borrowed', 'borrowed'),
    ]
    name = models.CharField(max_length=100, verbose_name='Book Name')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Price')
    description = models.TextField(verbose_name='Description')
    id = models.IntegerField(verbose_name='Book ID', primary_key=True)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    img = models.ImageField(upload_to='photos/%y/%m/%d', null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_book, default='available', verbose_name='Status')

    def __str__(self):
        return self.name
    
class Signup(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=20)
    confirmPassword = models.CharField(max_length=20)
    isAdmin = models.BooleanField(default=False)
    profilePicture = models.ImageField(default='default.jpg', upload_to='profilePictures')

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(Signup, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Book)
