import random
from django.core.management.base import BaseCommand
from faker import Faker
from project_app.models import Book, Category
from django.core.files.base import ContentFile
from urllib.request import urlopen
from io import BytesIO

class Command(BaseCommand):
    help = 'Generate fake books using the Faker library'

    def handle(self, *args, **kwargs):
        fake = Faker()

        categories = ['Programming', 'Novels']
        # categories = ['Fiction', 'Non-Fiction', 'Science', 'History', 'Fantasy', 'Biography']
        category_objects = []
        for category_name in categories:
            category = Category.objects.get_or_create(name=category_name)
            category_objects.append(category)

        for _ in range(10):
            # image_url = fake.image_url()
            image_url = f"https://picsum.photos/200/300"
            image_response = urlopen(image_url)
            image_file = BytesIO(image_response.read())
            image_name = f"{fake.word()}.jpg"

            book = Book(
                name=fake.sentence(nb_words=3),
                price=round(random.uniform(10, 100), 2),
                description=fake.text(max_nb_chars=200),
                author=fake.name(),
                category=random.choice(category_objects),
                status=random.choice(['available', 'borrowed'])
            )

            # book.save()

            book.img.save(image_name, ContentFile(image_file.getvalue()), save=True)

        self.stdout.write(self.style.SUCCESS('Successfully generated 10 books'))