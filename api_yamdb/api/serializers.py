from rest_framework import serializers
from django.utils import timezone
import re

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug', )


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id', 'rating',)


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=False,
                                            slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True,
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Genre.objects.all())
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id', 'rating',)
        lookup_field = 'genre__slug'

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
        if value < -3000:
            raise serializers.ValidationError(
                detail={
                    'year': 'Год не может быть ранее 3000 до Н.Э..'
                }
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'title', 'author', 'pub_date')
        model = Review

    def validate(self, data):
        """Проверка на уникальность отзыва от 1 автора для 1 произведения."""
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        author = request.user
        if (request.method == 'POST'
           and Review.objects.filter(author=author, title=title_id).exists()):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        model = Comment


class AdminCreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role',
                  )
        model = User
        read_only_fields = ('confirmation_code',)

    def validate_username(self, username):

        pattern = r'^[\w.@+-]+$'
        if username != 'me' and re.search(pattern, username):
            return username
        raise serializers.ValidationError(
            'Имя не может содержать специальные символы и не равно "me"')


class UserCreateSerializer(AdminCreateUserSerializer):

    class Meta:
        fields = ('username',
                  'email',
                  )
        model = User


class UserPathSerializer(AdminCreateUserSerializer):

    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  )
        model = User
