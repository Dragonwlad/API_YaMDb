from rest_framework import serializers
from django.shortcuts import get_object_or_404

from core.models import Category, Genre, Title, TitleGenre, Review, Comment
from core.models import Review

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category для CRUD операций"""
    class Meta:
        model = Category
        fields = ('name', )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre для CRUD операций"""
    class Meta:
        model = Genre
        fields = ('slug', )


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для получения списка произведений"""

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
    """Сериализатор модели Title для добавления нового произведения и внесения
    изменений в существующие произведения
    """
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
    """
    Сериализатор модели Title для получения подробных данных о произведении
    """

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
    """
    Сериализатор для модели Review.
    Позволяет представлять данные отзыва в JSON-формате.
    """

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """
        Проверяет данные отзыва на валидность и запрещает пользователям оставлять повторные отзывы.
        """
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение')
        return data
    
    # def validate(self, attrs):

class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    Позволяет представлять данные комментария в JSON-формате.
    """

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
