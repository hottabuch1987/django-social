from django.core.management.base import BaseCommand
from faker import Faker
from account.models import User
from datetime import datetime
import random
import os
from django.core.files.images import ImageFile

fake = Faker('ru_RU')
#file_path = '/Users/hottabych/Desktop/znakomstva/shop/core/shop/management/biographies.txt' #локальный путь
#photos_directory = '/Users/hottabych/Music/znakomstva/shop/core/shop/management/images_directory/' #локальный путь
#file_path = '/app/shop/management/biographies.txt'

file_path = '/root/django-social/core/shop/management/biographies.txt'
photos_directory = '/root/django-social/core/shop/management/images_directory/'

photos_list = sorted(os.listdir(photos_directory))

class Command(BaseCommand):
    help = 'Create fake user profiles'
    def get_random_bio(self):
        with open(file_path, 'r', encoding='utf-8') as file:
            bios = file.readlines()
            return random.choice(bios).strip()

    def handle(self, *args, **options):
        for _ in range(40):  # Создайте 10 фейковых пользователей, можно изменить на нужное количество
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                gender = fake.random_element(elements=('women', 'men')),
                friends_count = fake.random_int(min=10, max=200),
                online_status = fake.random_element(elements=(True, False)),
                like_count = fake.random_int(min=50, max=400),
                birth_date = fake.date_between(start_date='-40y', end_date='-18y'),
                date_joined=fake.date_time_between(start_date=datetime(2023, 1, 1), end_date='now'),
                bio=self.get_random_bio(),
                # Другие поля модели User, которые вы хотите заполнить
            )
            # Проверить, не превышает ли индекс i количество файлов
            if _ < len(photos_list):
                photo_filename = photos_list[_]
                photo_path = os.path.join(photos_directory, photo_filename)

                with open(photo_path, 'rb') as f:
                    user.avatar.save(photo_filename, ImageFile(f), save=True)


            user.set_password('password123')  # Установите фиксированный пароль для всех пользователей
            user.save()

        self.stdout.write(self.style.SUCCESS('Successfully created fake users'))
