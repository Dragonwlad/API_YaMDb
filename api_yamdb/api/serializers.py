from rest_framework import serializers
from django.shortcuts import get_object_or_404

from core.models import Category, Genre, Title, TitleGenre
from core.models import Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ('slug', )


class TitleListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True,
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Genre.objects.all())
    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
        
    
class TitleManageSerealizer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True,
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Genre.objects.all())
    class Meta:
        model = Title
        fields = ('name', 'description', 'year', 'genre', 'category')

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = get_object_or_404(Genre, slug=genre)
            TitleGenre.objects.create(
                genre=current_genre, title=title)
        return title
    

class TitleDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True,
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Genre.objects.all())
    class Meta:
        model = Title
        fields = ('name', 'description', 'year', 'genre', 'category', 'rating')

class ReviewSerializer(serializers.ModelSerializer):
    author=serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
    
    # def validate(self, attrs):

class CommentSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'pub_date')