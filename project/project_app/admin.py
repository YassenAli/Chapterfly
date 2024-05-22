from django.contrib import admin
from .models import *

# class PagesAdmin(admin.ModelAdmin):
#     list_display = ['name', 'author', 'category']
#     list_display_links = ['name']
#     search_fields = ['name', 'author', 'category'] #Search by title, author, or category
#     fields = ['name', 'price', 'category', 'description', 'available', 'author']


# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Signup)
# admin.site.register(PagesAdmin)
