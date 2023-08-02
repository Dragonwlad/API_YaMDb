<<<<<<< HEAD
=======
import re
>>>>>>> 9474fa5 (настроил users победил ошибки)
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

<<<<<<< HEAD

class UserCreateSerializer(serializers.ModelSerializer):
=======
    def validate_username(self, username):

        pattern = r'^[\w.@+-]+$'
        if username != 'me' and re.search(pattern, username):
            return username
        raise serializers.ValidationError(
                'Имя не может содержать специальные символы и не равно "me"')


class UserCreateSerializer(AdminCreateUserSerializer):
>>>>>>> 9474fa5 (настроил users победил ошибки)

    class Meta:
        fields = ['username',
                  'email',
                  ]
        model = User
<<<<<<< HEAD
        read_only_fields = ('confirmation_code',)


class UserPathSerializer(serializers.ModelSerializer):
=======


class UserPathSerializer(AdminCreateUserSerializer):
>>>>>>> 9474fa5 (настроил users победил ошибки)

    class Meta:
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  ]
        model = User
<<<<<<< HEAD
        read_only_fields = ('confirmation_code',)
=======
>>>>>>> 9474fa5 (настроил users победил ошибки)
