import os 
os.environ.setdefault('DJANGO_SSETTINGS_MODULE', 'first_project.settings')

import django
django.setup()

import random
from users.models import username, user_profile, edit_history
from faker import Faker

fake_generator = Faker()
usernames = ['dogeA', 'dogeB', 'dogeC', 'dogeD']

def add_username():
    addUsername = username.objects.get_or_create(username = random.choice(usernames))[0]
    addUsername.save()
    return addUsername

def populate(fake_data_amount):

    for entry in range(fake_data_amount):

        addUsername = add_username()

        fake_bio = fake_generator.address()
        fake_date = fake_generator.date()
        fake_url = fake_generator.url()

        userProfile = user_profile.objects.get_or_create(username = addUsername, bio = fake_bio, url = fake_url)

        editHistory = edit_history.objects