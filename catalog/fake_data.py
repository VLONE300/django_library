import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lesson25django.settings")
django.setup()


from catalog.models import Author, Country
from faker import Faker


fake = Faker()


for _ in range(100):
    country_name = fake.country()
    Country.objects.create(name=country_name)


countries = Country.objects.all()


for _ in range(200):
    author_data = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'pseudonym': fake.user_name(),
        'date_of_birth': fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=40),
        'country': fake.random_element(elements=countries)
    }

    if fake.random_int(min=1, max=9):
        author_data['date_of_death'] = fake.date_of_birth(tzinfo=None, minimum_age=1, maximum_age=40)

    Author.objects.create(**author_data)
