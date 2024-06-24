from .models import Category

def categories_processor(request):
    return {
        'category': Category.objects.all(),
    }
