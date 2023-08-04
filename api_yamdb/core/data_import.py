import csv
from django.shortcuts import get_object_or_404
from io import open
from django.http import HttpResponse

from reviews.models import Category, Genre, Title, TitleGenre, Review, Comment
from users.models import User


def category_import():
    with open(r'static\data\category.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'])
            except ImportError:
                print('Эта запись уже есть в базе')


def genre_import():
    with open(r'static\data\genre.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'])
            except ImportError:
                print('Эта запись уже есть в базе')


def title_import():
    with open(r'static\data\titles.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                category = get_object_or_404(Category, id=row['category'])
                Title.objects.get_or_create(id=row['id'],
                                            name=row['name'],
                                            year=row['year'],
                                            category=category)
            except ImportError:
                print('Эта запись уже есть в базе')


def genre_title_import():
    with open(r'static\data\genre_title.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                title = get_object_or_404(Title, id=row['title_id'])
                genre = get_object_or_404(Genre, id=row['genre_id'])
                TitleGenre.objects.get_or_create(
                    id=row['id'],
                    title=title,
                    genre=genre)
            except ImportError:
                print('Эта запись уже есть в базе')


def users_import():
    with open(r'static\data\users.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                User.objects.get_or_create(id=row['id'],
                                           username=row['username'],
                                           email=row['email'],
                                           role=row['role'],
                                           bio=row['bio'],
                                           first_name=row['first_name'],
                                           last_name=row['last_name'])
            except ImportError:
                print('Эта запись уже есть в базе')


def review_import():
    with open(r'static\data\review.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = get_object_or_404(Title, id=row['title_id'])
            author = get_object_or_404(User, id=row['author'])
            try:
                Review.objects.get_or_create(id=row['id'],
                                             title=title,
                                             text=row['text'],
                                             author=author,
                                             score=row['score'],
                                             pub_date=row['pub_date'])
            except ImportError:
                print('Эта запись уже есть в базе')


def comment_import():
    with open(r'static\data\comments.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            review = get_object_or_404(Review, id=row['review_id'])
            author = get_object_or_404(User, id=row['author'])
            try:
                Comment.objects.get_or_create(
                    id=row['id'],
                    review=review,
                    text=row['text'],
                    author=author,
                    pub_date=row['pub_date'])
            except ImportError:
                print('Эта запись уже есть в базе')


def data_import(request):
    category_import()
    genre_import()
    title_import()
    genre_title_import()
    review_import()
    comment_import()
    return HttpResponse('Данные импортированы!')
