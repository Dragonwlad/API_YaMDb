from django.shortcuts import render
import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import open


from core.models import Category, Genre, Title, TitleGenre, Review, Comment
from users.models import User
def data_import(request):

    
    with open('static\data\category.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Category.objects.get_or_create(id=row['id'],
                                           name=row['name'],
                                           slug=row['slug'])
            
    with open('static\data\genre.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)        
        for row in reader:
            Genre.objects.get_or_create(id=row['id'],
                                           name=row['name'],
                                           slug=row['slug'])
            
    with open(r'static\data\titles.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)        
        for row in reader:        
            category = get_object_or_404(Category, id=row['category'])
            Title.objects.get_or_create(id=row['id'],
                                           name=row['name'],
                                           year=row['year'],
                                           category=category)
            
    with open(r'static\data\genre_title.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)        
        for row in reader:        
            title = get_object_or_404(Title, id=row['title_id'])
            genre = get_object_or_404(Genre, id=row['genre_id'])
            TitleGenre.objects.get_or_create(id=row['id'],
                                           title=title,
                                           genre=genre)

    with open(r'static\data\users.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)       
        for row in reader:
            User.objects.get_or_create(id=row['id'],
                                           username=row['username'],
                                           email=row['email'],
                                           role=row['role'],
                                           bio=row['bio'],
                                           first_name=row['first_name'],
                                           last_name=row['last_name'])
    
    with open(r'static\data\review.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)        
        for row in reader:        
            title = get_object_or_404(Title, id=row['title_id'])
            author = get_object_or_404(User, id=row['author'])
            Review.objects.get_or_create(id=row['id'],
                                         title=title,
                                         text=row['text'],
                                         author=author,
                                         score=row['score'],
                                         pub_date=row['pub_date'])

    with open(r'static\data\comments.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)        
        for row in reader:
            review = get_object_or_404(Review, id=row['review_id'])
            author = get_object_or_404(User, id=row['author'])
            Comment.objects.get_or_create(id=row['id'],
                                         review=review,
                                         text=row['text'],
                                         author=author,
                                         pub_date=row['pub_date'])

    return HttpResponse('Данные импортированы')