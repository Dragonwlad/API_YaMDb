import re
from rest_framework import serializers

from users.models import User


class AdminCreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role',
                  ]
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
        fields = ['username',
                  'email',
                  ]
        model = User


class UserPathSerializer(AdminCreateUserSerializer):

    class Meta:
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  ]
        model = User
