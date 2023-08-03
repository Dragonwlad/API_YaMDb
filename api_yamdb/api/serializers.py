from django.db.models import Avg
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.utils import timezone

from reviews.models import Category, Genre, Title, TitleGenre, Review, Comment
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', )


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ('name', 'slug', )


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    class Meta:
        model = Title
        fields = ('id', 'category', 'description', 'genre', 'name', 'year')
        read_only_fields = ['id',]
        
    
# class TitleSerealizer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     genre = GenreSerializer(many=True)
#     class Meta:
#         model = Title
#         fields = ('id', 'name', 'year', 'rating',
#                   'description', 'genre', 'category')
#         read_only_fields = ('id', 'rating',)

#     def create(self, validated_data):
#         genres = validated_data.pop('genre')
#         title = Title.objects.create(**validated_data)
#         for genre in genres:
#             current_genre = get_object_or_404(Genre, slug=genre)
#             TitleGenre.objects.create(
#                 genre=current_genre, title=title)
#         return title
    

class TitleSerealizer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True,
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Genre.objects.all())
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        read_only_fields = ('id', 'rating',)

    def validate_year(self, value):
        """
        Проверка, что значение поля year меньше или равно текущему году.

        """
        if value > timezone.now().year:
            raise serializers.ValidationError(
                detail={
                    'year': 'Это поле не может быть больше текущего года.'
                }
            )
        return value
    
    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        rating_rounded = round(rating) if rating else rating
        return rating_rounded
    
    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = get_object_or_404(Genre, slug=genre)
            TitleGenre.objects.create(
                genre=current_genre, title=title)
        return title
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre'] = GenreSerializer(
            instance.genre,
            many=True,
        ).data
        representation['category'] = CategorySerializer(instance.category).data
        return representation

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("id", "title", "author", "pub_date")
        model = Review

    def validate(self, data):
        """Проверка на уникальность отзыва от одного автора для одного произведения."""
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        author = request.user
        if (request.method == 'POST'
           and Review.objects.filter(author=author, title=title_id).exists()):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение от одного автора.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("id", "author", "pub_date")
        model = Comment
